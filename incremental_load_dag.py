from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta

default_args = {
    'owner': 'olorunleke_white',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id = 'incremental_data_load', 
    description='An incremental DAG that moves changes daily',
    default_args=default_args, 
    schedule_interval=timedelta(days=1)
    ) as dag:
  	# Define task clean, running a cleaning job.
    load_data = BashOperator(
        task_id='incremental_load_bigquery',
        bash_command="python bigquery.py"
        )
