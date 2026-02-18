FROM apache/airflow:2.8.1

USER airflow
RUN pip install --no-cache-dir dbt-postgres==1.7.0 kagglehub
