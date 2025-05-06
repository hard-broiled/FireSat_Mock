import time

from apscheduler.events import JobExecutionEvent

from firesat.comm_protocol import ccsds_packet, downlink, uplink
from firesat.mission_model.event_generator import generate_mock_events
from firesat.mission_model.mission_data import MissionEvent
from firesat.scheduling_engine.scheduler_service import SchedulerService


def my_listener(event):
    if isinstance(event, JobExecutionEvent):
        job_id = event.job_id
        scheduled_run_time = event.scheduled_run_time
        retval = event.retval
        exception = event.exception
        traceback = event.traceback

        print(f"Job {job_id} executed at {scheduled_run_time}")
        if retval:
            print(f"Return value: {retval}")
        if exception:
            print(f"Exception: {exception}")
            print(f"Traceback: {traceback}")


def run_real_time_simulation():
    # testStore = []

    def sched_callback(event: MissionEvent, scheduledStore: list) -> None:  # TODO: should this return a lambda since it is intended to be passed to the scheduler?
        packet = uplink.convert_event_to_packet(event)
        encoded = uplink.send_uplink_packet(packet)  # "Packet sent successfully: packet.version = {response.version}", encodingResult)
        scheduledStore.append(encoded)

    def listener_callback(uplinkResults: tuple[str, bytes]) -> None:  # TODO: should this return a lambda since it is intended to be passed to the scheduler?
        # packet = downlink.receive_downlink_packet(uplinkResults[1])
        # room to process the recieved CCSDS_Packet here
        pass

    print("[Runner] Generating mission events...")
    events = generate_mock_events()

    print("[Runner] Scheduling mission events...")
    scheduler = SchedulerService()
    schedule = scheduler.schedule_events(events, uplink.send_uplink_packet)  # sched_callback(events, testStore))  # TODO: add uplink as the callback function

    print("[Runner] Starting simulation...")
    for event in schedule:
        print(f"[Sim] Executing Event: {event.id} at {event.timestamp}")
        packet = ccsds_packet.CCSDS_Packet(  # TODO: replace with the comm_protocol create packet function
            header=f"{event.id}_hdr",
            version=event.id,
            packet_type=event.event_type,
            apid=f"{event.id}-apid-spoofed",
            seq_count=f"{event.seq_count}-seq_count-spoofed",
            payload=str(event),
        )
        encoded = uplink.send_uplink_packet(packet)  # "Packet sent successfully: packet.version = {response.version}", encodingResult)
        response = downlink.receive_downlink_packet(encoded[1])  # "Packet received successfully: packet.version = {decodingResult.version}", decodingResult)
        print(f"[Sim] {response[0]}: {response[1]}")
        time.sleep(0.2)  # Simulated real-time delay


if __name__ == "__main__":
    run_real_time_simulation()
