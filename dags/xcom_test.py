import airflow
from airflow.operators.bash_operator import BashOperator
from airflow.operators import PythonOperator
from airflow.models import DAG,Variable
import datetime
from airflow.contrib.sensors.gcs_sensor  import GoogleCloudStorageObjectSensor



DAG_NAME = 'XCOM_TEST'
args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(10)
    }

# export AIRFLOW_VAR_FOO=BAR
# export AIRFLOW_VAR_FOO_BAZ='{"hello":"world"}'
Variable.set("foo","bar")
foo = Variable.get("foo")
# foo_json = Variable.get("foo_baz", deserialize_json=True)

print(foo)
# print(foo_json)

def push(**kwargs):
	return "x_com_value_with_push"

def pull(**kwargs):
	task_instance = kwargs['ti']
	xcom_var_val = task_instance.xcom_pull(key='push_1_key')
	print(xcom_var_val)


dag = DAG(
    dag_id=DAG_NAME,
	catchup=False,
    default_args=args,
    schedule_interval='25 10 * * *',
)

run_file_1 = BashOperator(
	task_id = 'run_file_1',
	bash_command = f'python /home/airflow/gcs/data/file_1.py',
	email_on_failure = False,
	dag = dag

	)


run_file_2 = BashOperator(
	task_id = 'run_file_2',
	bash_command = f"python /home/airflow/gcs/data/file_2.py",
	email_on_failure = False,
	dag= dag


	)

push_1 = PythonOperator(
	task_id = 'xom_push_try',
	provide_context = True,
	python_callable = push,
	dag= dag
	)

pull_1 = PythonOperator(
	task_id = 'xom_pull_try',
	provide_context = True,
	python_callable = pull,
	dag= dag
	)



x_com_push_try = BashOperator(
	task_id = 'bigquery_ls',
	bash_command = "bq ls",
	email_on_failure = False,
	dag= dag


	)



x_com_push_try>> run_file_1 >> [run_file_2, push_1 >> pull_1]