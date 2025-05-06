from firesat.comm_protocol import uplink
from firesat.mission_model.event_generator import generate_mock_events
from firesat.mission_model.mission_data import MissionEvent
from firesat.scheduling_engine.scheduler_service import SchedulerService


def test_event_to_packet_flow():
    # this method should be replaced with a process to convert the MissionEvent to a CCSDS_Packet and uplink it to the satellite
    def test_callback(event: MissionEvent) -> None:  # TODO: should this return a lambda since it is intended to be passed to the scheduler?
        packet = uplink.convert_event_to_packet(event)
        uplink.send_uplink_packet(packet)  # "Packet sent successfully: packet.version = {response.version}", encodingResult)

    events = generate_mock_events()
    scheduler = SchedulerService()
    scheduledJobs = scheduler.schedule_events(events, test_callback)

    for i in range(len(scheduledJobs)):
        # get callback result from each job in scheduledJobs
        # get the response message and packet back
        # verify the mission event is the same as what was encoded etc.
        # TODO: Enhancement to have uplink talk to a satellite spoof that takes the MissionEvent, and creates a MissionEventReceived data object or something along those lines to send back
        # decoded_packet = downlink.receive_downlink_packet(encoded[1])[1]
        # assert decoded_packet.header == packet.header
        # assert decoded_packet.payload == packet.payload

        jobId = scheduledJobs[i]
        job = scheduler.scheduler.get_job(jobId)
        job
