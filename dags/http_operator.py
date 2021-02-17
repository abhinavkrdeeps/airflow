from airflow import DAG
from airflow.operators import DummyOperator
from airflow.operators.http_operator import SimpleHttpOperator
import airflow
from airflow.sensors.http_sensor import HttpSensor


DAG_NAME = 'HTTP_OPERATOR_TEST'
args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(10)
    }



dag = DAG(
    dag_id=DAG_NAME,
	catchup=False,
    default_args=args,
    schedule_interval='3 12 * * *',
)


start_task = DummyOperator(
	task_id= 'starting_task',
	dag= dag
	)


http_sensor_task = HttpSensor(
	task_id = 'http_sensor_task',
	http_conn_id = 'https_default',
	method = 'GET',
	endpoint='dog.ceo/api/breed/hound/images',
    headers={"Content-Type": "application/json"},
    xcom_push=True,
    dag=dag

	)

t1 = SimpleHttpOperator(
    task_id='get_labrador',
    method='GET',
    http_conn_id='https_default',
    endpoint='dog.ceo/api/breed/hound/images',
    headers={"Content-Type": "application/json"},
    xcom_push=True,
    dag=dag)



http_sensor_task >> start_task >> t1
