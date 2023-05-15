from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash_operator import BashOperator

with DAG(
    'meu_primeiro_dag',
    start_date=days_ago(1),
    schedule_interval='@daily'
) as dag:
    tarefa_1 = EmptyOperator(task_id='primeira_tarefa_do_primeiro_dag')
    tarefa_2 = EmptyOperator(task_id='segunda_tarefa_do_primeiro_dag')
    tarefa_3 = EmptyOperator(task_id='terceira_tarefa_do_primeiro_dag')
    #vai_ser = SqlOperator()
    #também_será = KubbernetesOperator()
    tarefa_4 = BashOperator(
                            task_id='cria_pasta',
                            bash_command='mkdir -p "/home/v/Documents/airflowalura/pasta"'
    )

    tarefa_1 >> [tarefa_2, tarefa_3]
    tarefa_3 >> tarefa_4
    