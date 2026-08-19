import logging
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from apscheduler.schedulers.background import BackgroundScheduler

from blogboard.services.storage import R2StorageService
from blogboard.graph.graph import graph
from blogboard.services.dispatcher import dispatcher

logger = logging.getLogger(__name__)

class AutonomousScheduler:
    """
    Autonomous Background Scheduler service.
    Periodically checks domain publication history, picks stale domains,
    and runs the LangGraph article generation graph automatically.
    """

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False

    def today_ist(self) -> str:
        ist = timezone(timedelta(hours=5, minutes=30))
        return datetime.now(ist).strftime("%Y-%m-%d")

    def get_least_recently_updated_domain(self) -> str:
        """
        Scans Cloudflare R2 / Local storage registries and picks
        the domain with the oldest/least-recent publication date.
        """
        storage = R2StorageService()
        domain_dates = storage.get_all_domains_last_updated()
        
        # Sort domains by date string ("Never" or oldest YYYY-MM-DD comes first)
        sorted_domains = sorted(domain_dates.items(), key=lambda item: item[1])
        selected_domain = sorted_domains[0][0]
        logger.info(f"[SCHEDULER] Selected domain '{selected_domain}' (Last update: {sorted_domains[0][1]})")
        return selected_domain

    def run_automated_generation_job(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Core automated job function triggered on a schedule.
        """
        target_domain = domain or self.get_least_recently_updated_domain()
        date_str = self.today_ist()

        logger.info(f"\n=======================================================")
        logger.info(f"  [AUTOMATION] Triggering Scheduled Article Generation")
        logger.info(f"  Domain : {target_domain}")
        logger.info(f"  Date   : {date_str}")
        logger.info(f"=======================================================\n")

        initial_state = {
            "domain": target_domain,
            "date": date_str,
            "dry_run": False
        }
        config = {"configurable": {"thread_id": f"auto-{target_domain}-{date_str}"}}

        try:
            final_state = graph.invoke(initial_state, config=config)
            
            # Dispatch notifications & social threads
            dispatcher.dispatch_all(final_state)
            
            return final_state
        except Exception as e:
            logger.error(f"[AUTOMATION ERROR] Scheduled generation failed: {e}", exc_info=True)
            return {"error": str(e), "domain": target_domain}

    def start(self, interval_hours: int = 24):
        """
        Starts the background APScheduler daemon.
        """
        if self.is_running:
            logger.info("[SCHEDULER] Scheduler is already active.")
            return

        # Add interval job with immediate first execution
        self.scheduler.add_job(
            self.run_automated_generation_job,
            trigger="interval",
            hours=interval_hours,
            next_run_time=datetime.now(),
            id="daily_blog_generator",
            replace_existing=True
        )
        self.scheduler.start()
        self.is_running = True
        logger.info(f"🚀 [SCHEDULER] Background scheduler started! Running every {interval_hours} hours.")

    def stop(self):
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("[SCHEDULER] Scheduler stopped.")

auto_scheduler = AutonomousScheduler()
