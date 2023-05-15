from airflow.operators.sql import SqlOperator

select_sql = "SELECT * FROM path_video"

my_task = SqlOperator(
    task_id='my_task',
    sql=select_sql,
    database='my_mysql_conn',
    dag=my_dag
)
