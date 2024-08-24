import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#Imports from Prefect service
from prefect import flow
from prefect.deployments import Deployment
from prefect.client.schemas.schedules import IntervalSchedule
from datetime import timedelta, datetime

#Imports from modules of project
from ingestion.main import main as ingestion_main
from process.main import main as process_main

#With the functions correct imported, now create the workflow


@flow(name="Pipeline Climate",
      description="Pipeline workflow orquestration each 5 min")
def pipe_flow():
    ingestion_main()   
    process_main()

#This function control the flow of the other tasks
#Now defining the params of prefect workflow

#Scheduling
schedules = [ IntervalSchedule(
    interval=timedelta(minutes=5),
    anchor_date=datetime(2024, 8, 24, 1, 32)
)]

#Deployment
deploy = Deployment.build_from_flow(
    flow=pipe_flow,
    schedules=schedules,
    name="Pipeline Climate Deploy",
    work_queue_name="default"
)

if __name__ == "__main__":
    deploy.apply()