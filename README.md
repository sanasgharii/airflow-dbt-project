# Airflow + dbt + Postgres — End-to-End Data Pipeline

## Overview

This project is a fully containerized local data pipeline built using:

- **Airflow** → workflow orchestration  
- **dbt** → data transformation & testing  
- **Postgres** → data warehouse  
- **Docker Compose** → container orchestration  

The pipeline automatically:

1. Downloads a public retail dataset from Kaggle  
2. Loads it into Postgres  
3. Transforms the data using dbt (staging + mart layers)  
4. Runs data quality tests  
5. Produces analytical tables ready for reporting  

Everything runs locally inside Docker.

---

## How to Run

### 1. Build containers
docker compose build
### 2. Start services
docker compose up -d
### 3. Initialize Airflow (first time only)

Create admin user:

docker compose run airflow-webserver airflow users create \
  --username admin \
  --firstname Sana \
  --lastname Asghari \
  --role Admin \
  --email admin@example.com \
  --password admin



### 4. Open Airflow UI



http://localhost:8080


Login:


admin / admin


### 5. Trigger the DAG in Airflow webserver

Run:


dbt_pipeline


---

## Dataset

Dataset: **Customer Shopping Dataset**  
Source: Kaggle  

The dataset is automatically downloaded during pipeline execution.

CSV files are not stored in the repository to keep it lightweight.

---

## Example Insight

From the `fct_sales_monthly` table, we can analyze:

- Monthly revenue trends  
- Transaction volume changes over time  
- Average order value  
- Seasonality patterns  

This demonstrates how raw transactional data is transformed into business-ready metrics.

---

## Key Concepts Demonstrated

- Containerized data stack
- Service networking in Docker
- Workflow orchestration
- SQL-based transformation with dbt
- Data quality enforcement
- Layered data architecture (raw → staging → mart)
- Reproducible local environment

---

## Future Improvements

- Incremental dbt models
- LocalExecutor instead of SequentialExecutor
- Monitoring & alerting
- Cloud deployment
- Dashboard integration (Power BI / Tableau)

