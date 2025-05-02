from dataclasses import dataclass
from typing import Any


@dataclass
class CCSDS_Packet:
    header: str
    version: int
    packet_type: str  # e.g. "telemetry", "telecommand"
    apid: int
    seq_count: int
    payload: Any
    # Additional fields to be added as needed or found to be useful for the CCSDS standard
    # checksum: int; timestamp etc.
