# Using Airflow version 2.6.1
from airflow import DAG
from airflow.operators.python import get_current_context
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models.skipmixin import SkipMixin

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

# Function: returns an exception to fail the task if any tasks in the task_list have failed 
def overall_dag_status(task_list):
    context = get_current_context()
    for task_id in task_list:
        task_state = context["dag_run"].get_task_instance(task_id).state
        if task_state == "failed":
            raise Exception("Task {} failed. Failing this DAG run".format(task_id))

# Function: custom short circuit, skips only specified tasks
def custom_short_circuit(upstream_task_id, task_ids_to_skip):
    tasks_to_skip = []
    task_state = get_task_state(upstream_task_id)
    if task_state == "failed":
        context = get_current_context()
        for task_id in task_ids_to_skip:
            task = context["dag_run"].get_task_instance(task_id)
            tasks_to_skip.append(task) 
        if tasks_to_skip:
            SkipMixin().skip(dag_run=context['dag_run'], execution_date=context['ti'].execution_date, tasks=tasks_to_skip)

with DAG(
    dag_id="overall-dag-status",
    default_args=default_args,
    max_active_runs=1,
    catchup=False,
    default_view="graph",
    schedule_interval="@daily",
    tags=["demo-dags"]
) as dag:

    # Example bash task which will fail for the purposes of testing the overall_dag_state task
    # Purposefully given an incorrect bash_command to force task failure to trigger the short circuit
    first_task = BashOperator(
        task_id="first_task",
        bash_command="?echo \"this is the first task\""
    )

    # Custom short circuit task
    short_circuit = PythonOperator(
        task_id="short_circuit",
        provide_context=True,
        python_callable=custom_short_circuit,
        op_kwargs={"upstream_task_id": "first_task", "task_ids_to_skip": ["second_task"]},
        trigger_rule="all_done",
        dag=dag
    )

    # Example bash task to show that this task will get skipped when the short circuit is triggered
    second_task = BashOperator(
        task_id="second_task",
        bash_command="echo \"this is the second task\""
    )

    # Overall failure task
    # This task will not get skipped if the short circuit is triggered
    overall_dag_status = PythonOperator(
        task_id="overall_dag_status",
        provide_context=True,
        python_callable=overall_dag_status,
        op_kwargs={"task_list": ["first_task", "second_task"]},
        trigger_rule="all_done",
        dag=dag
    )
    (
        first_task >> short_circuit >> second_task >> overall_dag_status
    )