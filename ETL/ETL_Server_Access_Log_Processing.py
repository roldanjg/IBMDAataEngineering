# Task 1: Create the imports block.

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Joaquin Grau',
    'start_date': days_ago(0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# 'email': ['ramesh@somemail.com'],
# Task 3: Create the DAG definition block. The DAG should run daily.

dag = DAG(
    'ETL_Server_Access_Log_Processing',
    default_args=default_args,
    description='gets some data cool',
    schedule_interval=timedelta(days=1),
)

# define the tasks

# define the first task

downloadURL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt'
download = BashOperator(
    task_id='download',
    bash_command='wget "{}"'.format(downloadURL),
    dag=dag,
)

# define the second task
# define the task 'extract'

extract = BashOperator(
    task_id='extract',
    bash_command='cut -f1,4 -d"#" web-server-access-log.txt > /home/project/airflow/dags/extracted.txt',
    dag=dag,
)

# define the task 'transform'

transform = BashOperator(
    task_id='transform',
    bash_command='tr "[a-z]" "[A-Z]" < /home/project/airflow/dags/extracted.txt > /home/project/airflow/dags/capitalized.txt',
    dag=dag,
)

# define the task 'load'

load = BashOperator(
    task_id='load',
    bash_command='zip log.zip capitalized.txt' ,
    dag=dag,
)

# task pipeline

download >> extract >> transform >> load
# cp  ETL_Server_Access_Log_Processing.py $AIRFLOW_HOME/dags
# airflow dags list