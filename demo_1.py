from datetime import datetime
from airflow import DAG
from airflow.operators import PythonOperator


def first():
    print("first")


def second():
    print("second")


def third():
    print("third")


with DAG('demo_1', description='123', schedule_interval=None, start_date=datetime(2018, 1, 1), catchup=False) as dag:

    first = PythonOperator(
        task_id='first',
        python_callable=first,
        dag=dag,
    )

    second = PythonOperator(
        task_id='second',
        python_callable=second,
        dag=dag,
    )

    third = PythonOperator(
        task_id='third',
        python_callable=third,
        dag=dag,
    )

    first >> second >> third
