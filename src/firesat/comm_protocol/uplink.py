from .ccsds_packet import CCSDS_Packet
from .serialization import decode, encode


def send_uplink_packet(packet: CCSDS_Packet) -> tuple[str, bytes]:
    """Stubbed method to send a CCSDS packet to the satellite. In a real-world scenario, this would involve network communication."""

    # Simulate sending the packet (e.g., over a network)
    # In a real-world scenario, you would send the encoded data to the satellite and handle a response from that process
    # For now, we just encode, decode, and return the packet with a return message
    encodingResult = encode(packet)
    response = decode(encodingResult)
    return (f"Packet sent successfully: packet.header = {response.header}", encodingResult)
