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
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

# define the tasks

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command="tar -xzf /home/project/airflow/dags/finalassignment/staging/tolldata.tgz -C /home/project/airflow/dags/finalassignment/staging/",
    dag=dag,
)

# 
# define the task 

extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -f1,2,3,4 /home/project/airflow/dags/finalassignment/staging/vehicle-data.csv \
         > /home/project/airflow/dags/finalassignment/staging/csv_data.csv',
    dag=dag,
)

# define the task 'transform'

extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command="cut -f5,6,7 -d$'\t' /home/project/airflow/dags/finalassignment/staging/tollplaza-data.tsv | sed -e 's/\t/,/g' \
         > /home/project/airflow/dags/finalassignment/staging/tsv_data.csv",
    dag=dag,
)

# define the task 'load'

extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command="sed -e 's/\s\+/,/g' /home/project/airflow/dags/finalassignment/staging/payment-data.txt |cut -f11,12 -d','\
        > /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv",
    dag=dag,
)

consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command="paste -d',' /home/project/airflow/dags/finalassignment/staging/csv_data.csv /home/project/airflow/dags/finalassignment/staging/tsv_data.csv /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv > /home/project/airflow/dags/finalassignment/staging/extracted_data.csv",
    dag=dag
)

transform_data = BashOperator(
    task_id='transform_data',
bash_command='tr "[a-z]" "[A-Z]" < /home/project/airflow/dags/finalassignment/staging/extracted_data.csv> /home/project/airflow/dags/finalassignment/staging/transformed_data.csv',
    dag=dag
)

# task pipeline

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data
 	
 	

# cp  ETL_Server_Access_Log_Processing.py $AIRFLOW_HOME/dags
# airflow dags list
# airflow dags unpause process_web_log