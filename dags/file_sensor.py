from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.dummy_operator    import DummyOperator
from airflow.contrib.sensors.gcs_sensor  import GoogleCloudStorageObjectSensor
import datetime
from datetime import date, timedelta
from airflow.models import DAG,Variable
import airflow

DAG_NAME = 'File_Sensor'

args = {
    'owner': 'Datametica',
    'start_date': airflow.utils.dates.days_ago(90)
    }


dag = DAG(
    dag_id=DAG_NAME,
    catchup=False,
    default_args=args,
    schedule_interval=None
)

start_task  = DummyOperator(
    task_id= "start",
    dag = dag
     )

# sensor_task = FileSensor(
#     task_id= "file_sensor_task", 
#     poke_interval= 30,
#     filepath= "/home/" )

gcs_file_sensor = GoogleCloudStorageObjectSensor(
    task_id='gcs_file_sensor',
    bucket='dataflow_poc11',
    object='gs://dataflow_poc11/task1.csv', 
    timeout=120,
    dag =dag)

final_task = DummyOperator(
    task_id='final_task',
    dag =dag

    )
start_task >> gcs_file_sensor >>final_task