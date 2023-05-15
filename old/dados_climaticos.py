from airflow import DAG
import pendulum
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import os
from os.path import join
import pandas as pd
from datetime import datetime, timedelta

with DAG(
        "dados_climaticos",
        start_date=pendulum.datetime(2022, 8, 22, tz="UTC"),
        schedule_interval='0 0 * * 1', # executar toda segunda feira
    ) as dag:

    tarefa_1 = BashOperator(
        task_id = 'cria_pasta',
        bash_command = 'mkdir -p "/home/millenagena/Documents/airflowalura/semana"'
    )

    def extrai_dados():
        # intervalo de datas
        data_inicio = datetime.today()
        data_fim = data_inicio + timedelta(days=7)

        # formatando as datas
        data_inicio = data_inicio.strftime('%Y-&m-&d')
        data_fim = data_fim.strftime('%Y-%m-%d')

        city = 'Boston'
        key = 'ANZQ5K8QQP8BXZ85F4EQ2FPK'

        URL = join('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/',
        f'{city}/{data_inicio}/{data_fim}?unitGroup=metric&include=days&key={key}&contentType=csv')

        dados = pd.read_csv(URL)
        print(dados.head())

        file_path = f'home/millenagena/Documents/datapipeline/semana={data_inicio}/'
        os.mkdir(file_path)

        dados.to_csv(file_path + 'dados_brutos.csv')
        dados[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(file_path + 'temperaturas.csv')
        dados[['datetime', 'description', 'icon']].to_csv(file_path + 'condicoes.csv')

    tarefa_2 = PythonOperator(
        task_id = 'extrai_dados',
        python_callable = extrai_dados
    )

    tarefa_1 >> tarefa_2