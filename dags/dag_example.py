from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import time

default_args = {
    'owner': 'kenny'
}

with DAG(
  "test",
  start_date=days_ago(1),
  schedule_interval=None,
  default_args=default_args
) as dag:

    def x(t=10):
      time.sleep(t)

    begin_t = PythonOperator(task_id="begin_task", python_callable=x)
    task_a = DummyOperator(task_id="task_a")
    task_b = DummyOperator(task_id="task_b")
    task_c = DummyOperator(task_id="task_c")
    task_d = DummyOperator(task_id="task_d")

    begin_t >> task_a
    task_a >> [task_b, task_c]
    task_c >> task_d