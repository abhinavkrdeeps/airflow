from datetime import datetime, date
from airflow import DAG
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import BashOperator


dag = DAG('test_2',
          description='Test 2',
          catchup=False,
          schedule_interval= None,
          start_date=datetime(2020, 8, 1))

def python1():
	return 2;

dummy1 = PythonOperator(
    task_id='starting_task',
    python_callable=python1,
    dag=dag
)

dummy2 = BashOperator(
    task_id='branch1',
    bash_command="echo 3",
    dag=dag
)

dummy3 = BashOperator(
    task_id='branch2',
    bash_command="sleep 50",
    dag=dag
)

dummy4 = BashOperator(
    task_id='join_1',
    bash_command="echo 2",
    dag=dag
)

dummy5 = BashOperator(
    task_id='join_2',
    bash_command="echo 3",
    dag=dag
)

dummy1 >> [dummy2, dummy3] >> dummy4 >> dummy5