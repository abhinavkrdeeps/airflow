from datetime import datetime, date
from airflow import DAG
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
from airflow.operators.dummy_operator import DummyOperator

dag = DAG('test_branches',
          description='Test branches',
          catchup=False,
          schedule_interval='0 0 * * *',
          start_date=datetime(2018, 8, 1))


def python1():
    return "success"
    # print 'Test success'


dummy1 = PythonOperator(
    task_id='python1',
    python_callable=python1,
    dag=dag
)


dummy2 = DummyOperator(
    task_id='dummy2',
    dag=dag
)


dummy3 = DummyOperator(
    task_id='dummy3',
    dag=dag,
    trigger_rule='one_success'
)


def is_saturday():
    if date.today().weekday() == 6:
        return 'dummy2'
    else:
        return 'today_is_not_saturday'


branch_on_saturday = BranchPythonOperator(
    task_id='branch_on_saturday',
    python_callable=is_saturday,
    dag=dag)


not_saturday = DummyOperator(
    task_id='today_is_not_saturday',
    dag=dag
)

dummy1 >> branch_on_saturday >> dummy2 >> dummy3
branch_on_saturday >> not_saturday >> dummy3