from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    dag_id="dbt_raw",
    start_date=datetime(2026, 9, 9),
    schedule=None,   # manual trigger
    catchup=False,
) as dag:

    # Bronze
    raw = BashOperator(
        task_id="raw",
        bash_command="""
        source /mnt/d/mini-project/venv/bin/activate &&
        cd /mnt/d/mini-project/scrapping/data &&
        python countries.py
        """
    )   

    trigger_dbt = TriggerDagRunOperator(
        task_id="trigger_dbt_pipeline",
        trigger_dag_id="dbt_pipeline"
    )

    raw >> trigger_dbt