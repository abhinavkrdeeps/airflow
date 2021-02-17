import airflow
from airflow.operators.bash_operator import BashOperator
from airflow.operators import PythonOperator
from airflow.models import DAG,Variable
import datetime
from airflow.operators.sensors import ExternalTaskSensor



DAG_NAME = 'External_Task_Sensor_Test'
args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(10) 
     }


dag = DAG(
    dag_id=DAG_NAME,
	catchup=False,
    default_args=args,
    schedule_interval='25 10 * * *',
)

def dummy_call(**kwargs):
	return "Nothing to do.."

start_task = PythonOperator(
	task_id = 'start_task',
	python_callable = dummy_call,
	provide_context = True,
	dag = dag
	)

external_task_dependent = ExternalTaskSensor(
    task_id='dependent_on_dag_2_task',
    external_dag_id='XCOM_TEST',
    external_task_id='run_file_2',
    dag=dag) 

end_task = PythonOperator(
	task_id = 'end_task',
	python_callable = dummy_call,
	provide_context = True,
	dag = dag
	)

start_task >> external_task_dependent >> end_task