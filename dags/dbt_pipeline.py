from airflow import DAG
from datetime import datetime
from cosmos import DbtTaskGroup
from cosmos.config import ProfileConfig, ProjectConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

profile_config = ProfileConfig(
    profile_name="my_project",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgres_default",
        profile_args={
            "schema": "public",
        },
    ),
)

with DAG(
    dag_id="dbt_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    dbt_task_group = DbtTaskGroup(
        group_id="dbt_models",
        project_config=ProjectConfig(
            "/opt/airflow/dbt/my_project",
        ),
        profile_config=profile_config,
        operator_args={
            "install_deps": True,
        },
    )