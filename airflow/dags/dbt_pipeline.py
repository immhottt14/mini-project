from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="dbt_pipeline",
    start_date=datetime(2026, 9, 9),
    schedule=None,   # manual trigger
    catchup=False,
) as dag:

    # Bronze
    bronze = BashOperator(
        task_id="bronze_models",
        bash_command="cd /mnt/d/mini-project/mini-proj/models && dbt run --select bronze"
    )

    # Silver
    silver = BashOperator(
        task_id="silver_models",
        bash_command="cd /mnt/d/mini-project/mini-proj/models && dbt run --select silver"
    )

    # Gold/Datamart
    gold = BashOperator(
        task_id="gold_models",
        bash_command="cd /mnt/d/mini-project/mini-proj/models && dbt run --select gold"
    )

    bronze >> silver >> gold