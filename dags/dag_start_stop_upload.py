from airflow import DAG
import pendulum
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import os
from os.path import join
import pandas as pd
from datetime import datetime, timedelta
from requests import post, get 

with DAG(
        "dag_start_stop_upload",
        start_date=pendulum.datetime(2022, 8, 22, tz="UTC"),
        schedule_interval='20 8 * * *', # executar toda segunda feira
    ) as dag:

    def start_record():
        endpoint = "http://localhost:5000/start_recording"
        post(endpoint).json()
    def stop():
        endpoint_stop = "http://localhost:5000/stop_recording"
        post(endpoint_stop).json()
    def list_videos():
        endpoint_list = "http://localhost:5000/videos_gravados"
        get(endpoint_list).json()
    def upload():
        endpoint_upload = "http://localhost:5000/upload_video"
        post(endpoint_upload)

    tarefa_1 = PythonOperator(
                              task_id = 'start_record',
                              python_callable = start_record
                            )

    tarefa_2 = PythonOperator(
        task_id = 'stop_record',
        python_callable = stop
    )

    tarefa_3 = PythonOperator(
        task_id = 'list_videos',
        python_callable = list_videos
    )

    tarefa_4 = PythonOperator(
        task_id = 'send_video_to_s3',
        python_callable = upload
    )

    tarefa_1 >> tarefa_2
    tarefa_2 >> tarefa_3
    tarefa_3 >> tarefa_4