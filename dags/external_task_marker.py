import datetime

from airflow import DAG
from airflow.operators import DummyOperator
from airflow.sensors.external_task_sensor import ExternalTaskMarker, ExternalTaskSensor

start_date = datetime.datetime(2015, 1, 1)

with DAG(
    dag_id="external_task_marker_parent",
    start_date=start_date,
    schedule_interval='10 11 * * *',
) as parent_dag:
    
    parent_task = ExternalTaskMarker(
        task_id="parent_task",
        external_dag_id="external_task_marker_child",
        external_task_id="child_task1",
    )
   

with DAG(
    dag_id="external_task_marker_child",
    start_date=start_date,
    schedule_interval='20 11 * * *',
    
) as child_dag:
    
    child_task1 = ExternalTaskSensor(
        task_id="child_task1",
        external_dag_id=parent_dag.dag_id,
        external_task_id=parent_task.task_id
        # timeout=600,
        # allowed_states=['success'],
        # failed_states=['failed', 'skipped'],
        # mode="reschedule",
    )
    # [END howto_operator_external_task_sensor]
    child_task2 = DummyOperator(task_id="child_task2")
    child_task1 >> child_task2