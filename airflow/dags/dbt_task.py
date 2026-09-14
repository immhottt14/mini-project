from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'lamhot',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    dag_id='data_pipeline_dag',
    default_args=default_args,
    description='End-to-end data pipeline DAG',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    # 1. Scrapping data
    scrapping_task = BashOperator(
        task_id='scrapping_data',
        bash_command='python /app/get_raw_data.py'
    )

    # 2. DBT transform (bronze → silver → gold)
    dbt_task = BashOperator(
        task_id='dbt_transform',
        bash_command='dbt run --project-dir /usr/app'
    )

    # 3. Load ke Snowflake (via DBT sudah otomatis)
    snowflake_task = BashOperator(
        task_id='snowflake_load',
        bash_command='echo "Data loaded to Snowflake via DBT"'
    )

    # 4. Refresh Metabase (trigger API call)
    metabase_task = BashOperator(
        task_id='refresh_metabase',
        bash_command='curl -X POST http://metabase:3000/api/card/refresh'
    )

    # Orkestrasi urutan
    scrapping_task >> dbt_task >> snowflake_task >> metabase_task