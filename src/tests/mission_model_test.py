import time
from datetime import datetime

from firesat.mission_model.event_generator import generate_mock_events


def test_generate_mock_events():
    start_time = datetime.fromtimestamp(time.time() + 2)
    events = generate_mock_events(start_time)
    assert len(events) == 3
    assert events[0].timestamp > start_time
