from firesat.comm_protocol.ccsds_packet import CCSDS_Packet
from firesat.comm_protocol.downlink import receive_downlink_packet
from firesat.comm_protocol.serialization import decode, encode
from firesat.comm_protocol.uplink import send_uplink_packet


# serialization test class
def test_encode_decode_packet():
    packet = CCSDS_Packet(
        version=1,
        packet_type="telemetry",
        apid=100,
        seq_count=42,
        payload={"temp": 120},
    )
    encoded = encode(packet)
    decoded = decode(encoded)
    assert decoded == packet


# uplink test class
def test_uplink_simulation():
    packet = CCSDS_Packet(
        version=21,
        packet_type="telecommand",
        apid=101,
        seq_count=1,
        payload="activate",
    )
    response = send_uplink_packet(packet)
    assert f"Packet sent successfully: packet.version = {packet.version}" in response


# downlink test class
def test_downlink_simulation():
    packet = CCSDS_Packet(
        version=3,
        packet_type="telemetry",
        apid=102,
        seq_count=2,
        payload={"status": "ok"},
    )
    encodedPacket = encode(packet)
    response = receive_downlink_packet(encodedPacket)
    assert f"Packet received successfully: packet.version = {packet.version}" in response
