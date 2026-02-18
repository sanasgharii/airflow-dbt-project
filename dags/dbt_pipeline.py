from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="dbt_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    download_dataset = BashOperator(
        task_id="download_dataset",
        bash_command="""
        python - <<EOF
import kagglehub
import shutil
import os

path = kagglehub.dataset_download(
    "mehmettahiraslan/customer-shopping-dataset"
)

source_file = os.path.join(path, "customer_shopping_data.csv")
destination_folder = "/opt/airflow/dbt/my_project/seeds"
destination_file = os.path.join(destination_folder, "customer_shopping_data.csv")

os.makedirs(destination_folder, exist_ok=True)
shutil.copy(source_file, destination_file)

print("Dataset downloaded and moved.")
EOF
        """
    )

    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command="cd /opt/airflow/dbt && dbt seed --project-dir my_project --profiles-dir ."
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt && dbt run --project-dir my_project --profiles-dir ."
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt && dbt test --project-dir my_project --profiles-dir ."
    )

    download_dataset >> dbt_seed >> dbt_run >> dbt_test
