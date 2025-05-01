import json

from .ccsds_packet import CCSDS_Packet

# from .telecommand_packet import TelecommandPacket
# from .telemetry_packet import TelemetryPacket


def encode(packet: CCSDS_Packet) -> bytes:
    """Encodes a CCSDS packet into bytes for transmission."""

    # Convert the packet to a dictionary
    # Expanding this out for now for potential new features etc.
    # This is a simple example; in a real-world scenario, you would need to handle errors and validate the data
    packet_dict = {
        "version": packet.version,
        "packet_type": packet.packet_type,
        "apid": packet.apid,
        "seq_count": packet.seq_count,
        "payload": packet.payload,
    }
    return json.dumps(packet_dict).encode("utf-8")


def decode(data: bytes) -> CCSDS_Packet:
    """Decodes bytes into a CCSDS packet."""

    # Decode the bytes to a string and then parse it as JSON
    packet_dict = json.loads(data.decode("utf-8"))

    # Create a CCSDS_Packet object from the dictionary
    # Expanding this out for now for potential new features etc.
    # This is a simple example; in a real-world scenario, you would need to handle errors and validate the data
    return CCSDS_Packet(
        version=packet_dict["version"],
        packet_type=packet_dict["packet_type"],
        apid=packet_dict["apid"],
        seq_count=packet_dict["seq_count"],
        payload=packet_dict["payload"],
    )
