# Function to generate and return a mock list of MissionEvents with timestamps

from datetime import datetime, timedelta, timezone

from .mission_data import MissionEvent


def generate_mock_events(start_time: datetime = None) -> list[MissionEvent]:
    start = start_time or datetime.now(timezone.utc)
    return [
        MissionEvent(
            id="evt-001",
            timestamp=start + timedelta(seconds=1),
            event_type="observation",
            target="Wildfire A",
        ),
        MissionEvent(
            id="evt-002",
            timestamp=start + timedelta(seconds=1),
            event_type="downlink",
            target="Ground Station Alpha",
        ),
        MissionEvent(
            id="evt-003",
            timestamp=start + timedelta(seconds=1),
            event_type="observation",
            target="Wildfire B",
        ),
    ]
