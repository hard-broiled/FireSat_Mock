from ..mission_model.mission_data import MissionEvent
from .ccsds_packet import CCSDS_Packet
from .serialization import decode, encode

# pre-class design notes:
#   Driving function to be 'uplink'? uplink responsible for sending any packets, and can do that via the send uplink packet methods
#   Stretch goal of having the class take in a collection of missionevents or packets, it would then convert any events into packets, order them, and then send all packets
#       held within the packet container sequentially


def convert_event_to_packet(event: MissionEvent) -> CCSDS_Packet:
    """Converts a mission event to a CCSDS packet."""
    # In a real-world scenario, this would involve more complex logic to convert the event to a packet
    # For now, we just return the event as a packet
    packet = CCSDS_Packet(
        header=f"{event.id}_hdr",
        version=6,  # event.id,
        packet_type=event.event_type,
        apid=5,  # f"{event.id}-apid-spoofed",
        seq_count=3,  # "hardcoded-seq_count-spoofed",
        payload=str(event),
    )
    return packet


def send_uplink_packet(packet: CCSDS_Packet | MissionEvent) -> tuple[str, bytes]:
    """Stubbed method to send a CCSDS packet to the satellite. In a real-world scenario, this would involve network communication.
    Currently overloaded to accept either a CCSDS_Packet or a MissionEvent for ease of use.
    """

    # Simulate sending the packet (e.g., over a network)
    # In a real-world scenario, you would send the encoded data to the satellite and handle a response from that process
    # For now, we just encode, decode, and return the packet with a return message
    if isinstance(packet, CCSDS_Packet):
        encodingResult = encode(packet)
        response = decode(encodingResult)
    else:  # isinstance(packet, MissionEvent)
        packet = convert_event_to_packet(packet)
        encodingResult = encode(packet)
        response = decode(encodingResult)
    return (f"Packet sent successfully: packet.header = {response.header}", encodingResult)
