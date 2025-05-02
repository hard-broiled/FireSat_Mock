# test CLI execution for the scheduling service engine leveraging the mock events provided by the event generator module.
# poetry run python src/firesat/simulation_cli.py

import logging
import time

from firesat.mission_model.event_generator import generate_mock_events
from firesat.scheduling_engine.scheduler_service import SchedulerService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_event(event):
    logger.info(f"[EVENT EXECUTED] ID={event['id']} | Payload={event.get('payload')}")


def main():
    logger.info("=== Firesat Mission CLI ===")
    events = generate_mock_events()
    scheduler = SchedulerService()

    scheduler.start()
    scheduler.schedule_events(events, callback=handle_event)

    try:
        logger.info("Scheduler running. Waiting for events to execute...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Exiting CLI...")
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    main()
