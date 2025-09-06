from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.dates import days_ago
from datetime import timedelta

from utils.load_data import load_data
from utils.preprocess_data import preprocess_data
from utils.experiment import experiment
from utils.track_experiments_info import track_experiments_info
from utils.fit_best_model import fit_best_model
from utils.save_batch_data import save_batch_data

default_args = {
    "owner": "Shuvam Dutta",
    "depends_on_past": False,
    "email_on_failure": True,  # set to True if you want alerts
    "email": ["nicolo_albanese@outlook.it"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": days_ago(1),
}

with DAG(
    "ml_pipeline",
    description="ML pipeline example",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    tags=["ml", "training"],
) as dag:

    # 1️⃣ Create storage structures
    with TaskGroup("storage") as storage:
        create_experiment_table = PostgresOperator(
            task_id="create_experiment_tracking_table",
            postgres_conn_id="postgres_default",
            sql="sql/create_experiments.sql",
        )

        create_batch_table = PostgresOperator(
            task_id="create_batch_data_table",
            postgres_conn_id="postgres_default",
            sql="sql/create_batch_data_table.sql",
        )

    # 2️⃣ Fetch raw data
    fetch_data = PythonOperator(
        task_id="fetching_data",
        python_callable=load_data,
    )

    # 3️⃣ Prepare data
    with TaskGroup("prep") as prep:
        preprocess = PythonOperator(
            task_id="preprocessing",
            python_callable=preprocess_data,
        )

        save_batch = PythonOperator(
            task_id="saving_batch_data",
            python_callable=save_batch_data,
        )

        # Ensure preprocessing runs before saving
        preprocess >> save_batch

    # 4️⃣ Hyperparameter tuning
    tuning = PythonOperator(
        task_id="hyperparam_tuning",
        python_callable=experiment,
    )

    # 5️⃣ Post cross-validation tasks
    with TaskGroup("post_cv") as post_cv:
        save_results = PythonOperator(
            task_id="saving_results",
            python_callable=track_experiments_info,
        )

        fit_best = PythonOperator(
            task_id="fitting_best_model",
            python_callable=fit_best_model,
        )

    # Set pipeline order
    storage >> fetch_data >> prep >> tuning >> post_cv
