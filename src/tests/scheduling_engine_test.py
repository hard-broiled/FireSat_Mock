import os
import subprocess
import sys
import time

from firesat.mission_model.mission_data import MissionEvent
from firesat.scheduling_engine.scheduler_service import SchedulerService


# Test class for scheduler service
def test_schedule_single_event():
    scheduler = SchedulerService()
    scheduler.start()

    executed = []

    test_event = MissionEvent(
        id="test-event",
        timestamp=time.time() + 3,  # fire 2 seconds in the future
        event_type="communication",
        target="hello",
    )

    # test method that will be called when the event is executed, light simulation of just adding the event to a scheduled event store
    def test_callback(event: MissionEvent, scheduledStore: list):
        scheduledStore.append(event)

    scheduler.schedule_events([test_event], test_callback(test_event, executed))
    time.sleep(5)  # wait for execution
    scheduler.shutdown()

    assert len(executed) == 1
    assert executed[0]["id"] == "test-event"
    assert executed[0]["payload"] == "hello"


# Test class for simulation cli
def test_simulation_cli_runs_briefly():
    """Ensure the CLI starts up and runs for a short time."""
    cli_path = os.path.join("src", "firesat", "scheduling_engine", "simulation_cli.py")

    proc = subprocess.Popen([sys.executable, cli_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        # Let it run for 2 seconds
        time.sleep(2)
        proc.terminate()
        proc.wait(timeout=2)
    except Exception:
        proc.kill()
        raise
    finally:
        stdout, stderr = proc.communicate()

    # Basic assertion that CLI started up
    assert b"Firesat Mission CLI" in stdout or stderr
