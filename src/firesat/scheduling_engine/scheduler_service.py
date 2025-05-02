import logging
from datetime import datetime
from typing import Any, Callable, Dict, List

from apscheduler.executors.pool import ThreadPoolExecutor  # ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

"""
SchedulerService class wraps APScheduler to provide a simple interface for scheduling tasks.
Ability to:
    - Accept mission events
    - Schedule jobs for each event
    - Simulate real-time via event callbacks
    - Targets include graceful shutdown and logging
"""


class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler(executors={"default": ThreadPoolExecutor(5)})

    def start(self) -> Any:
        logger.info("Initializing SchedulerService.. ")
        self.scheduler.start()

    def shutdown(self) -> Any:
        logger.info("Shutting down SchedulerService..")
        self.scheduler.shutdown(wait=True)

    # This method adds the event to the apscheduler job queue
    def add_job(self, func, trigger, **kwargs) -> Any:
        job = self.scheduler.add_job(func, trigger, **kwargs)
        return job

    def remove_job(self, job_id) -> str:
        self.scheduler.remove_job(job_id)
        return "Job removed"

    def schedule_events(self, events: List[Dict], callback: Callable) -> None:
        """
        Schedules a list of events with datetime timestamps

        :param events: List of dicts representing individual events, each event having at least 'id' and 'timestamp' keys
        :param callback: Function to call with the event payload when triggered
        """
        # for each event, validate the timestamp, if valid then schedule the job
        for event in events:
            event_time = event.get("timestamp")
            if not isinstance(event_time, datetime):
                logger.warning(f"Invalid event timestamp: {event_time}. Event with id: {event['id']} will not be scheduled.", exc_info=True)
                continue

            logger.info(f"Scheduling event with id: {event['id']} at {event_time}.")
            self.add_job(
                func=callback,
                trigger="date",
                run_date=event_time,
                args=[event],  # Pass the event as an argument to the callback
                id=str(event["id"]),  # Use event id as job id
                replace_existing=True,  # Replace existing job with the same id
                # misfire_grace_time = 60,  # Allow a grace period of 60 seconds for the job to be executed
            )
