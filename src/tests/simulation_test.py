from firesat.comm_protocol import ccsds_packet, downlink, uplink
from firesat.mission_model.event_generator import generate_mock_events
from firesat.scheduling_engine.scheduler_service import SchedulerService


def test_event_to_packet_flow():
    events = generate_mock_events()
    scheduler = SchedulerService()
    schedule = scheduler.schedule_events(events)

    for event in schedule:
        packet = ccsds_packet.CCSDS_Packet(header=f"{event['id']}_hdr", payload=str(event))
        encoded = uplink.send_uplink_packet(packet)  # "Packet sent successfully: packet.version = {response.version}", encodingResult)
        decoded_packet = downlink.receive_downlink_packet(encoded[1])[1]

        assert decoded_packet.header == packet.header
        assert decoded_packet.payload == packet.payload
