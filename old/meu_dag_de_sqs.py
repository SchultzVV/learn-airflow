from airflow import DAG
from airflow.providers.amazon.aws.operators.sqs import SQSOperator
from datetime import datetime
import boto3

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 9)
}

with DAG('sqs_example', default_args=default_args, schedule_interval=None) as dag:

    send_sqs_message = SQSOperator(
        task_id='send_sqs_message',
        queue_url='https://sqs.us-east-1.amazonaws.com/123456789012/my-queue',
        message_body='Hello from Airflow!',
        aws_conn_id='aws_default'
    )
