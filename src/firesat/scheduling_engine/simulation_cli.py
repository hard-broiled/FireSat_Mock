# test CLI execution for the scheduling service engine leveraging the mock events provided by the event generator module.
# poetry run python src/firesat/simulation_cli.py

import logging
import time

from firesat.mission_model.event_generator import generate_mock_events
from firesat.mission_model.mission_data import MissionEvent
from firesat.scheduling_engine.scheduler_service import SchedulerService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def schedCallBack(event: MissionEvent):
    logger.info(f"[EVENT EXECUTED] ID={event.id} | Target={event.target}")


def main():
    logger.info("=== Firesat Mission CLI ===")
    events = generate_mock_events()
    scheduler = SchedulerService()

    scheduler.start()
    scheduledJobs = scheduler.schedule_events(events, callback=schedCallBack)

    try:
        logger.info(f"Scheduler running. Waiting for {len(scheduledJobs)} jobs to execute...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Exiting CLI...")
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    main()
