# Import the operator
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import date, timedelta

# # Set the path for our files.
# entry_point = "./bigquery.py"

default_args = {
    'owner': 'olorunleke_white',
    'depends_on_past': False,
    'start_date': date.today(),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id = 'full_data_load', 
    default_args=default_args, 
    schedule_interval=None
    ) as dag:
  	# Define task clean, running a cleaning job.
    load_data = BashOperator(
        task_id='full_load_bigquery',
        bash_command="python bigquery.py"
        )
