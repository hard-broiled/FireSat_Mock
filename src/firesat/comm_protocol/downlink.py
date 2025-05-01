from typing import Any

from .ccsds_packet import CCSDS_Packet
from .serialization import decode


def receive_downlink_packet(data: bytes) -> tuple[str, CCSDS_Packet, Any]:
    """Stubbed method to receive a CCSDS packet from the satellite. In a real-world scenario, this would involve network communication."""

    # Simulate receiving the packet (e.g., over a network)
    # In a real-world scenario, you would receive the encoded data from the satellite
    # For this example, we'll just decode the data
    decodingResult = decode(data)
    # returning a tuple that includes a success message, and the decoded packet
    return (f"Packet received successfully: packet.version = {decodingResult.version}", decodingResult)
