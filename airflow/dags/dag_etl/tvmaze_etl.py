import datetime
import pendulum
from textwrap import dedent
import os

from airflow import DAG
# from airflow import XComArg
# from airflow.models import Variable
# from airflow.operators.bash import BashOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.amazon.aws.operators.ecs import EcsOperator 
# from airflow.operators.python import PythonOperator
# from function.etl import extract, transform, load
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

with DAG(
        dag_id='tvmaze_etl',
        schedule_interval='0 0 * * *',
        start_date=pendulum.datetime(2022, 11, 1, tz="UTC"),
        catchup=False,
        render_template_as_native_obj=True,
        dagrun_timeout=datetime.timedelta(minutes=5),
        tags=['tvmaze'],
) as dag:

    etl_start = SlackWebhookOperator(
            task_id="etl_start",
            http_conn_id="tvmaze-slack-connection",
            message="ETL started",
            channel="#project2-group2"
        )

    etl_end = SlackWebhookOperator(
            task_id="etl_end",
            http_conn_id="tvmaze-slack-connection",
            message="ETL ended",
            channel="#project2-group2"
        )

    # maybe put into variables
    airflow_airbyte_conn_id = "tvmaze-airbyte-connection"
    airbyte_tvmazeapisf_conn_id = "52806ce8-bb8f-49d9-897d-9db5d62268a6"

    airbyte_trigger_sync = AirbyteTriggerSyncOperator(
        task_id='airbyte_trigger_sync',
        airbyte_conn_id=airflow_airbyte_conn_id,
        connection_id=airbyte_tvmazeapisf_conn_id,
        asynchronous=False,
        timeout=3600,
        wait_seconds=3
    )

    dbt_ecs_trigger = EcsOperator(
    task_id="dbt_ecs_trigger",
    dag=dag,
    aws_conn_id="aws-login-for-ecs-task",
    cluster="tvmaze-dbt-ecs-cluster",
    task_definition="tvmaze-dbt-ecs-task",
    launch_type="EC2",
    overrides={
        "containerOverrides": [
            {
                "name": "tvmaze-dbt-ecr-container",
            },
        ],
    },
    )

    etl_start >> airbyte_trigger_sync >> dbt_ecs_trigger >> etl_end