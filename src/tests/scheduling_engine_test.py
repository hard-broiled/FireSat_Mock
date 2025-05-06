import os
import subprocess
import sys
import time
from datetime import datetime

from firesat.comm_protocol.uplink import send_uplink_packet
from firesat.mission_model.event_generator import generate_mock_events
from firesat.mission_model.mission_data import MissionEvent
from firesat.scheduling_engine.scheduler_service import SchedulerService


# Test class for scheduler service
class TestSchedulerService:
    def setup(self):
        """Setup method to initialize the SchedulerService before each test."""
        self.scheduler = SchedulerService()
        self.scheduler.start()

    def test_schedule_single_event(self):
        scheduler = SchedulerService()
        scheduler.start()

        test_event = MissionEvent(
            id="test-event-1",
            timestamp=datetime.fromtimestamp(time.time() + 2),  # fire 2 seconds in the future
            event_type="communication",
            target="hello",
        )

        def simpleSchedCallBack(event: MissionEvent):
            print(f"[EVENT EXECUTED] ID={event.id} | Target={event.target}")

        scheduledJobs = scheduler.schedule_events(events=[test_event], callback=simpleSchedCallBack)
        time.sleep(1)  # wait for execution
        scheduler.shutdown()

        assert len(scheduledJobs) == 1
        assert scheduledJobs[0].id == test_event.id

    def test_schedule_multiple_events(self):
        def simpleSchedCallBack(event: MissionEvent):
            print(f"[EVENT EXECUTED] ID={event.id} | Target={event.target}")

        scheduler = SchedulerService()
        scheduler.start()

        gen_events = generate_mock_events()

        scheduledjobs = scheduler.schedule_events(events=gen_events, callback=simpleSchedCallBack)
        time.sleep(1)  # wait for execution
        scheduler.shutdown()

        assert len(scheduledjobs) == len(gen_events)
        for job in scheduledjobs:
            assert job.id in [event.id for event in gen_events]

    def test_schedule_uplink_event(self):
        scheduler = SchedulerService()
        scheduler.start()

        test_event = MissionEvent(
            id="test-event-1",
            timestamp=datetime.fromtimestamp(time.time() + 2),  # fire 2 seconds in the future
            event_type="communication",
            target="hello",
        )

        scheduledJobs = scheduler.schedule_events(events=[test_event], callback=send_uplink_packet)
        time.sleep(1)  # wait for execution
        scheduler.shutdown()

        assert len(scheduledJobs) == 1
        assert scheduledJobs[0].id == "test-event-1"

    def test_schedule_multiple_uplink_events(self):
        scheduler = SchedulerService()
        scheduler.start()

        gen_events = generate_mock_events()

        scheduledjobs = scheduler.schedule_events(events=gen_events, callback=send_uplink_packet)
        time.sleep(1)  # wait for execution
        scheduler.shutdown()

        assert len(scheduledjobs) == len(gen_events)
        for job in scheduledjobs:
            assert job.id in [event.id for event in gen_events]

    def test_simulation_cli_runs_briefly(self):
        """Ensure the CLI starts up and runs for a short time."""
        cli_path = os.path.join("src", "firesat", "scheduling_engine", "simulation_cli.py")

        proc = subprocess.Popen([sys.executable, cli_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            # Let it run for 2 seconds
            time.sleep(1)
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            proc.kill()
            raise
        finally:
            stdout, stderr = proc.communicate()

        # Basic assertion that CLI started up
        assert b"Firesat Mission CLI" in stdout or stderr
