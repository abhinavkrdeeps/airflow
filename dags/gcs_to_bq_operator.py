from typing import Any

import airflow
from airflow import models
from airflow.operators import bash_operator

gcs_to_bq = None  # type: Any
try:
    from airflow.contrib.operators import gcs_to_bq
except ImportError:
    pass


if gcs_to_bq is not None:
    args = {
        'owner': 'Datametica',
        'start_date': airflow.utils.dates.days_ago(2)
    }

    dag = models.DAG(
        dag_id='gcs_to_bq_operator', default_args=args,
        schedule_interval=None)

    create_test_dataset = bash_operator.BashOperator(
        task_id='create_airflow_test_dataset_1',
        bash_command='bq mk airflow_test_1',
        dag=dag)

    # [START howto_operator_gcs_to_bq]
    load_csv = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id='gcs_to_bq_example',
        bucket='dataflow_poc11',
        source_objects=['task1.csv'],
        destination_project_dataset_table='gcs-bq.airflow_test.gcs_to_bq_table_1',
        schema_fields=[
            {'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'post_abbr', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'post_abbr1', 'type': 'STRING', 'mode': 'NULLABLE'},

        ],
        write_disposition='WRITE_TRUNCATE',
        dag=dag)
    # [END howto_operator_gcs_to_bq]



    create_test_dataset >> load_csv 