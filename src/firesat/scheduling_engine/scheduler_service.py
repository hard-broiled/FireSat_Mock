import logging
from datetime import datetime
from typing import Any, Callable, List

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler

from firesat.mission_model.mission_data import MissionEvent

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
:Responsibility: Schedule Mission Events from Ground Station to be sent to a satellite
"""


class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler(executors={"default": ThreadPoolExecutor(5)})

    def start(self) -> Any:
        logger.info("Initializing  SchedulerService..")
        try:
            self.scheduler.start()
            logger.info("SchedulerService initialized successfully.")
        except Exception:
            logger.error("Error during SchedulerService initialization: {e}", exc_info=True)

    def shutdown(self) -> Any:
        logger.info("Shutting down SchedulerService..")
        try:
            self.scheduler.shutdown(wait=True)
            logger.info("SchedulerService shut down successfully.")
        except Exception:
            logger.error("Error during SchedulerService shut down: {e}", exc_info=True)

    # This method adds the event to the apscheduler job queue
    def add_job(self, func: Callable, trigger: str, **kwargs) -> Job:
        # Note for fun: The func argument can be given either as a callable object or a textual reference in the package.module:some.object format,
        # where the first half (separated by :) is an importable module and the second half is a reference to the callable object, relative to the module.
        #   idea: just supply the importable reference to an uplink method that accepts a MissionEvent, converts it to a packet, and uplinks it

        try:
            logger.info(f"Adding job with id: {kwargs.get('id')} to the scheduler.")
            job = self.scheduler.add_job(func, trigger, **kwargs)
            logger.info(f"Job with id: {job.id} added successfully.")
        except Exception as e:
            logger.error(f"Failed to add job with id: {kwargs.get('id')}. Error: {e}", exc_info=True)

        return job

    def remove_job(self, job_id) -> str:
        self.scheduler.remove_job(job_id)
        return "Job removed"

    def schedule_events(self, events: List[MissionEvent], callback: Callable, **kwargs) -> list[Job]:
        """
        Schedules a list of events with datetime timestamps.

        :param events: List of dicts representing individual events, each event having at least 'id' and 'timestamp' keys
        :param callback: Function to call with the event payload when triggered
        :kwargs: Additional keyword arguments to pass to the callback function
        :return: List of successfully scheduled jobs
        """
        # for each event, validate the timestamp, if valid then schedule the job
        logger.info(f"Attempting to schedule {len(events)} events.")
        scheduledJobs = []
        for event in events:
            event_time = event.timestamp
            current_time = datetime.now(event_time.tzinfo) if event_time.tzinfo else datetime.now()
            # Currently not validating the event type, but this can be added in the future if needed
            if not isinstance(event_time, datetime):
                logger.warning(f"Invalid event timestamp: {event_time}. Event with id: {event.id} will not be scheduled.", exc_info=True)
                continue
            elif event_time <= current_time:
                logger.warning(f"Provided event timestamp is in the past. ID: {event.id} Event Timestamp: {event_time}. Current Time {current_time} Event will not be scheduled.", exc_info=True)
                continue
            else:
                logger.info(f"Scheduling event with id: {event.id} at {event_time}.")
                try:
                    job = self.add_job(
                        func=callback,
                        trigger="date",
                        run_date=event_time,
                        args=[event],  # Pass the event as an argument to the callback
                        kwargs=kwargs,  # Additional keyword arguments to pass to the callback
                        id=str(event.id),  # Use event id as job id
                        replace_existing=True,  # Replace existing job with the same id
                    )
                    scheduledJobs.append(job)
                    logger.info(f"Event with id: {event.id} scheduled successfully. Job id: {job.id}.")
                except Exception as e:
                    logger.error(f"Failed to schedule event with id: {event.id}. Error: {e}", exc_info=True)
                    continue
        logger.info(f"Scheduled {len(scheduledJobs)} events successfully.")
        return scheduledJobs  # Return the list of scheduled jobs for verification
