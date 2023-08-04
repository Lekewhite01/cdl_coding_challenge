from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlToGoogleCloudStorageOperator
from airflow.providers.google.cloud.transfers.mysql_to_gcs import MySQLToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

default_args = {
    'owner': 'olorunleke_white',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_full_load',
    default_args=default_args,
    schedule_interval=None,  # Set your desired schedule interval
)

mysql_to_gcs = MySqlToGoogleCloudStorageOperator(
    task_id='mysql_to_gcs',
    sql='SELECT * FROM employees',
    bucket='your_gcs_bucket',
    filename='employees_data.json',
    mysql_conn_id='mysql_connection',
    google_cloud_storage_conn_id='gcs_connection',
    dag=dag,
)

gcs_to_bigquery = GCSToBigQueryOperator(
    task_id='gcs_to_bigquery',
    bucket='your_gcs_bucket',
    source_objects=['employees_data.json'],
    destination_project_dataset_table='your_project.your_dataset.employees',
    autodetect=True,
    bigquery_conn_id='bigquery_connection',
    google_cloud_storage_conn_id='gcs_connection',
    dag=dag,
)

mysql_to_gcs >> gcs_to_bigquery
