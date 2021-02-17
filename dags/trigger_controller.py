from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id="Trigger_Controller_Dag",
    default_args={"owner": "airflow"},
    start_date=days_ago(2),
    schedule_interval="@once"
) as dag:

    trigger = TriggerDagRunOperator(
        task_id="test_trigger_dagrun",
        trigger_dag_id="example_trigger_target_dag",  # Ensure this equals the dag_id of the DAG to trigger
        conf={"message": "Hello World"},
    )