import os
import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from blogboard.services.scheduler import auto_scheduler
from blogboard.services.storage import R2StorageService
from blogboard.graph.graph import graph
from blogboard.services.dispatcher import dispatcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("blogboard-api")

from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Agentic Blog Engine REST API",
    description="Autonomous Multi-Agent Content Generation & Publishing Gateway",
    version="1.0.0"
)

# Enable CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TriggerRequest(BaseModel):
    domain: Optional[str] = Field(None, description="Category domain (ml, dl, nlp, cv, genai, statistics, ainews)")
    topic: Optional[str] = Field(None, description="Specific article title or topic to generate")
    dry_run: bool = Field(False, description="Preview mode (skip LLM generation & storage writes)")

class TriggerResponse(BaseModel):
    status: str
    message: str
    domain: Optional[str]
    topic: Optional[str]

@app.on_event("startup")
def startup_event():
    """Starts the background scheduler daemon automatically on server boot."""
    auto_scheduler.start(interval_hours=24)
    logger.info("🚀 BlogBoard FastAPI Gateway booted successfully!")

@app.on_event("shutdown")
def shutdown_event():
    """Stops the scheduler gracefully."""
    auto_scheduler.stop()

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "BlogBoard AI Engine",
        "scheduler_active": auto_scheduler.is_running
    }

@app.get("/api/v1/status")
def get_status():
    storage = R2StorageService()
    last_updated = storage.get_all_domains_last_updated()
    return {
        "scheduler_active": auto_scheduler.is_running,
        "domains_last_updated": last_updated,
        "server_status": "online"
    }

def run_generation_task(domain: Optional[str], topic: Optional[str], dry_run: bool):
    initial_state = {"dry_run": dry_run}
    if domain:
        initial_state["domain"] = domain
    if topic:
        initial_state["topic"] = topic

    config = {"configurable": {"thread_id": "api-trigger"}}
    final_state = graph.invoke(initial_state, config=config)
    
    if not dry_run:
        dispatcher.dispatch_all(final_state)

@app.post("/api/v1/trigger", response_model=TriggerResponse)
def trigger_generation(payload: TriggerRequest, background_tasks: BackgroundTasks = None):
    """
    Triggers an immediate article generation process.
    Can be called by webhooks, n8n workflows, or frontend triggers.
    """
    target_domain = payload.domain or auto_scheduler.get_least_recently_updated_domain()
    target_topic = payload.topic or "Autonomous Selection"

    if background_tasks:
        background_tasks.add_task(run_generation_task, target_domain, payload.topic, payload.dry_run)
        message = "Article generation task launched in background."
    else:
        run_generation_task(target_domain, payload.topic, payload.dry_run)
        message = "Article generation completed synchronously."

    return TriggerResponse(
        status="success",
        message=message,
        domain=target_domain,
        topic=target_topic
    )

# Mount web frontend at root URL using absolute path
web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web"))
if os.path.exists(web_dir):
    app.mount("/", StaticFiles(directory=web_dir, html=True), name="static")

