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
    'owner': 'JG',
    'start_date': days_ago(0),
    'email':'lala@lala.es',
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# 'email': ['ramesh@somemail.com'],
# Task 3: Create the DAG definition block. The DAG should run daily.

dag = DAG(
    'process_web_log',
    default_args=default_args,
    description='pipeline that analyzes the web server log file, extracts the required lines(ending with html) and fields(time stamp, size ) and transforms (bytes to mb) and load (append to an existing file.)',
    schedule_interval=timedelta(days=1),
)

firsttask = BashOperator(
    task_id='extract_data',
    bash_command="cut -f1 -d' ' /home/project/airflow/dags/capstone/accesslog.txt > /home/project/airflow/dags/capstone/extracted_data.txt",
    dag=dag,
)

secondttask = BashOperator(
    task_id='transform_data',
    bash_command="grep -v '198.46.149.143' /home/project/airflow/dags/capstone/extracted_data.txt > /home/project/airflow/dags/capstone/transformed_data.txt",
    dag=dag,
)

# define the task 'load'
thirdtask = BashOperator(
    task_id='load_data',
bash_command='tar cvf /home/project/airflow/dags/capstone/weblog.tar /home/project/airflow/dags/capstone/transformed_data.txt',
    dag=dag
)

# task pipeline

firsttask >> secondttask >> thirdtask
 	
 	
# cp  process_web_log.py $AIRFLOW_HOME/dags
# airflow dags list
# airflow dags unpause process_web_log