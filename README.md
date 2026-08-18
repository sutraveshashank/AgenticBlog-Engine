# 🚀 BlogBoard AI — Autonomous Multi-Agent Content Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-orange.svg)](https://www.langchain.com/langgraph)
[![Groq LLM](https://img.shields.io/badge/Groq-gpt--oss--120b-purple.svg)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**BlogBoard AI** is an enterprise-grade, fully autonomous multi-agent content creation, validation, publishing, and social media distribution platform.

Powered by **LangGraph** stateful cyclic DAG execution, **FastAPI** REST API Gateway, **APScheduler** background daemon, and **Groq** high-speed LLM inference, BlogBoard automatically researches, drafts, validates, publishes, and broadcasts deep-dive technical articles across 7 domains (`ML`, `DL`, `NLP`, `CV`, `Gen AI`, `Stats`, `AI News`).

---

## 🌟 Key Features

- 🤖 **Stateful Multi-Agent Architecture (LangGraph)**
  - **TutorialAgent**: Conducts web research (Tavily / The Guardian API) and drafts technical tutorials.
  - **NewsAgent**: Gathers real-time AI news headlines and synthesizes editorial summaries.
  - **ValidatorAgent**: Functions as an automated supervisor reviewing technical accuracy, completeness, and H1 structure in a cyclic revision loop.

- ⏰ **Autonomous APScheduler Daemon**
  - Runs in the background 24/7.
  - Automatically identifies stale/least-recently updated categories and generates fresh articles without human intervention.

- 🌐 **FastAPI REST API Gateway & Swagger Docs**
  - Includes `POST /api/v1/trigger`, `GET /api/v1/status`, and `GET /api/v1/health`.
  - Interactive Swagger UI dashboard live at `http://localhost:8000/docs`.

- 📱 **Multi-Channel Notification & Social Dispatcher**
  - Formats ready-to-post **Twitter/X Threads** and **LinkedIn Posts** saved to `output/social/`.
  - Supports Discord, Slack, and Telegram webhooks.

- 🔗 **n8n Workflow Integration Template**
  - Includes a 1-click [`n8n_blogboard_workflow.json`](n8n_blogboard_workflow.json) template for no-code automation.

- 💾 **Dual-Mode Abstraction Storage Layer**
  - Zero-config **Local Filesystem** storage under `blogboard/web/blogs/`.
  - Optional production support for **Cloudflare R2** S3-compatible object storage.

- 🎨 **Modern Dark-Mode Web Frontend**
  - Pure HTML/CSS/JS client-side Markdown parser (Marked.js) with syntax highlighting (Highlight.js), reading time indicators, and cache-busting.

---

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph "External Triggers & Ingress"
        A1["⏰ APScheduler Background Daemon"] --> B["FastAPI Gateway (/api/v1/trigger)"]
        A2["⚡ Webhook / n8n Workflow"] --> B
        A3["💻 CLI (python run.py)"] --> B
    end

    subgraph "LangGraph Cyclic Multi-Agent Core"
        B --> C{"Domain Router"}
        C -- "Technical Domain" --> D["TutorialAgent"]
        C -- "AI News Domain" --> E["NewsAgent"]
        D --> F["ValidatorAgent (Supervisor)"]
        E --> F
        F -- "Draft Rejected (Revision Loop)" --> D
        F -- "Approved" --> G["R2StorageService"]
    end

    subgraph "Publishing & Distribution Layer"
        G --> H["💾 Local Filesystem (blogboard/web/blogs/)"]
        G --> I["☁️ Cloudflare R2 Object Bucket"]
        G --> J["📣 NotificationDispatcher"]
        J --> K["🐦 Twitter/X Thread (.json)"]
        J --> L["💼 LinkedIn Post (.json)"]
        J --> M["💬 Discord / Slack Webhooks"]
    end

    subgraph "Frontend Layer"
        H --> N["🌐 BlogBoard Web UI (http://localhost:8000/)"]
    end
```

---

## 📁 Repository Structure

```text
BlogBoard-AI-Blog-Generator/
├── blogboard/
│   ├── agents/
│   │   ├── tutorial_agent/    # Tutorial drafting agent & prompts
│   │   ├── news_agent/        # Real-time AI news agent & prompts
│   │   └── validator_agent/   # Supervisor validation agent
│   ├── api/
│   │   └── app.py             # FastAPI Gateway server & static mounting
│   ├── config/
│   │   └── settings.py        # Pydantic environment configuration
│   ├── graph/
│   │   ├── graph.py           # LangGraph compiled StateGraph workflow
│   │   └── state.py           # BlogState TypedDict definition
│   ├── services/
│   │   ├── dispatcher.py      # Multi-channel social media & webhook dispatcher
│   │   ├── scheduler.py       # Autonomous APScheduler background service
│   │   └── storage.py         # Dual-mode R2 & local storage engine
│   ├── tools/
│   │   ├── tavily_search.py   # Tavily Web Research Tool
│   │   └── guardian_search.py # The Guardian API Search Tool
│   ├── web/                   # Dark-mode static frontend (HTML/CSS/JS)
│   └── run.py                 # Core CLI & Server entrypoint
├── output/                    # Local storage fallback & social thread outputs
├── n8n_blogboard_workflow.json# 1-Click n8n Workflow integration JSON
├── run_server.ps1             # 1-Click PowerShell launcher script
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## ⚡ Quick Start

### 1️⃣ Clone the Repository & Setup Virtual Environment

```powershell
git clone https://github.com/sutraveshashank/AgenticBlog-Engine.git
cd AgenticBlog-Engine/BlogBoard-AI-Blog-Generator

# Create & activate virtual environment
python -m venv myenv
..\myenv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
LLM__API_KEY=your_groq_api_key_here
LLM__MODEL_NAME=openai/gpt-oss-120b
STORAGE__R2_ACCOUNT_ID=dummy
STORAGE__R2_ACCESS_KEY_ID=dummy
STORAGE__R2_SECRET_ACCESS_KEY=dummy
STORAGE__R2_BUCKET_NAME=dummy
```

---

## 🚀 Running the Engine

### Option A: Launch Server & Background Scheduler (Recommended)

Run the 1-click launcher:

```powershell
.\run_server.ps1
```

Or using python:

```powershell
python blogboard/run.py --serve
```

- 🌐 **Web Frontend**: [http://localhost:8000/](http://localhost:8000/)
- 📄 **Interactive Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option B: Run On-Demand Single Article Generation via CLI

```powershell
# Autonomous topic selection
python blogboard/run.py

# Specific topic & domain
python blogboard/run.py --topic "Understanding Diffusion Models in Generative AI" --domain "genai"
```

---

### Option C: Trigger via Webhook API (PowerShell / cURL / n8n)

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/trigger" -Method Post -Body '{"domain":"nlp", "topic":"Large Language Model Tokenization"}' -ContentType "application/json"
```

---

## 📊 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Serves the interactive BlogBoard Web UI |
| `/docs` | `GET` | Interactive Swagger API documentation |
| `/api/v1/trigger` | `POST` | Triggers immediate article generation (optional `domain`, `topic`, `dry_run`) |
| `/api/v1/status` | `GET` | Returns scheduler status & last updated dates per domain |
| `/api/v1/health` | `GET` | Health check endpoint |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
