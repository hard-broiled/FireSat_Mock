import time

from firesat.comm_protocol import ccsds_packet, downlink, uplink
from firesat.mission_model.event_generator import generate_mock_events
from firesat.scheduling_engine.scheduler_service import SchedulerService


def run_real_time_simulation():
    print("[Runner] Generating mission events...")
    events = generate_mock_events()

    print("[Runner] Scheduling mission events...")
    scheduler = SchedulerService()
    schedule = scheduler.schedule_events(events)

    print("[Runner] Starting simulation...")
    for event in schedule:
        print(f"[Sim] Executing Event: {event['id']} at {event['timestamp']}")
        packet = ccsds_packet.CCSDS_Packet(
            header=f"{event['id']}_hdr",
            version=event["id"],
            packet_type=event["event_type"],
            apid=f"{event['id']}-apid-spoofed",
            seq_count=f"{event['seq_count']}-seq_count-spoofed",
            payload=str(event),
        )
        encoded = uplink.send_uplink_packet(packet)  # "Packet sent successfully: packet.version = {response.version}", encodingResult)
        response = downlink.receive_downlink_packet(encoded[1])  # "Packet received successfully: packet.version = {decodingResult.version}", decodingResult)
        print(f"[Sim] {response[0]}: {response[1]}")
        time.sleep(0.2)  # Simulated real-time delay


if __name__ == "__main__":
    run_real_time_simulation()
