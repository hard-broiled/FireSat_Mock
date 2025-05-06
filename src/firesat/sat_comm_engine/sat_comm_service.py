# import logging
# from datetime import datetime
# import time
# from typing import Any, Callable, List

# from apscheduler.executors.pool import ThreadPoolExecutor
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.job import Job
# from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent

# from firesat.mission_model.mission_data import MissionEvent
# from firesat.comm_protocol.uplink import send_uplink_packet
# from firesat.comm_protocol.downlink import receive_downlink_packet

# # Initialize logger
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


# def listener(self, schedEvent: JobExecutionEvent, trigger: str, **kwargs) -> Job:
#     try:
#         if not schedEvent.exception:
#             logger.info(f"Adding downlink listener job for scheduled job with id: {schedEvent.job_id}")
#             schedRetVal = schedEvent.retval

#             # add a downlink job for each uplink job
#             listenerJob = self.add_job(
#                 func=receive_downlink_packet,
#                 trigger=trigger,
#                 run_date=datetime.fromtimestamp(time.time() + 2),
#                 args=[schedRetVal],
#                 kwargs=kwargs,
#                 id=f"{str(schedEvent.job_id)}-listener",  # Use event id as job id + listener
#                 replace_existing=True,
#             )
#         else:
#             logger.warning(f"JobExecutionEvent Seen: {schedEvent.exception}")
#     except Exception:
#         logger.error(f"Failed to add listener to scheduled job. ID: {schedEvent.job_id}")

#     return listenerJob


# def listener(self, schedEvent: JobExecutionEvent, trigger: str, **kwargs) -> Job:
#     try:
#         if not schedEvent.exception:
#             logger.info(f"Adding downlink listener job for scheduled job with id: {schedEvent.job_id}")
#             schedRetVal = schedEvent.retval

#             # add a downlink job for each uplink job
#             listenerJob = self.add_job(
#                 func=receive_downlink_packet,
#                 trigger=trigger,
#                 run_date=datetime.fromtimestamp(time.time() + 2),
#                 args=[schedRetVal],
#                 kwargs=kwargs,
#                 id=f"{str(schedEvent.job_id)}-listener",  # Use event id as job id + listener
#                 replace_existing=True,
#             )
#         else:
#             logger.warning(f"JobExecutionEvent Seen: {schedEvent.exception}")
#     except Exception:
#         logger.error(f"Failed to add listener to scheduled job. ID: {schedEvent.job_id}")

#     return listenerJob
