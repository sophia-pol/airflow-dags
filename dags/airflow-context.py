# Using Airflow version 2.6.1
from airflow import DAG
from airflow.operators.python import get_current_context
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Default dag arguments
# Update owner with the given user
default_args = {
    "owner": "this_user",
    "depends_on_past": False,
    "start_date": "2024-07-08"
}

# Function: Determines the state of a given task
def get_task_state(task_id):
    context = get_current_context()
    task_state = context["dag_run"].get_task_instance(task_id).state
    print(f"Task state of {task_id} is {task_state}")
    return task_state

with DAG(
    dag_id="airflow-context",
    default_args=default_args,
    max_active_runs=1,
    catchup=False,
    default_view="graph",
    schedule_interval="@daily",
    tags=["demo-dags"]
) as dag:

    # Example bash task
    first_task = BashOperator(
        task_id="first_task",
        bash_command="echo \"this is the first task\""
    )

    # Task that reads the previous task's state
    task_state = PythonOperator(
        task_id="task_state",
        provide_context=True,
        python_callable=get_task_state,
        op_kwargs={"task_id": "first_task"},
        trigger_rule="all_done",
        dag=dag
    )
    (
        first_task >> task_state
    )