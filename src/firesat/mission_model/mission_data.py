# Initially Defining data classes for Satellite, Instrument, and MissionEvent

# Also add features to potentially create hardcoded or YAML/JSON-generated list of simulated mission events, satellite, and instrument data. etc.

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Satellite:
    id: str
    name: str
    launch_date: datetime


@dataclass
class Instrument:
    id: str
    name: str
    type: str
    satellite_id: str


@dataclass
class MissionEvent:
    id: str
    timestamp: datetime
    event_type: str  # e.g. "observation", "downlink"
    target: Optional[str] = None


# @dataclass
# class Orbit:
#     id: str
#     satellite_id: str
#     start_time: datetime
#     end_time: datetime
#     altitude: float
#     inclination: float
