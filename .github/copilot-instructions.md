## Quick context

- This repository combines Airflow (for orchestration) and dbt (for analytics models) using Docker Compose.
- Services (see `docker-compose.yml`):
  - `postgres` (Postgres 14) — database for Airflow and dbt
  - `airflow` (Apache Airflow 2.8.1) — webserver mounted to `./dags`
  - `dbt` (dbt-postgres image) — working directory `/usr/app` is mounted to the repo `./dbt`

## Big-picture architecture

- Data plane: dbt models live in `dbt/my_project/models/` and compile into `dbt/target/` (compiled SQL, `manifest.json`, `run_results.json`).
- Orchestration plane: Airflow expects DAGs in the repository `dags/` (mounted into the container). Currently `dags/` is empty in this workspace, but the docker-compose setup maps `./dags` -> `/opt/airflow/dags`.
- Integration point: dbt talks to the `postgres` service on the Docker network; this repo’s `dbt/profiles.yml` uses `host: postgres`, which works when running dbt from inside the `dbt` container.

## Primary developer workflows (concrete commands)

- Start the stack (Postgres + Airflow webserver mounted to local `dags/`):

```sh
docker-compose up -d
# Airflow UI: http://localhost:8080
```

- Run dbt inside the provided dbt container (profiles.yml is in `dbt/`, working dir inside container is `/usr/app`):

```sh
docker-compose run --rm dbt dbt run --profiles-dir .
docker-compose run --rm dbt dbt test --profiles-dir .
```

Notes:
  - `--profiles-dir .` points dbt at the `dbt/profiles.yml` included in the repo volume.
  - If you run dbt from your host machine (not in the `dbt` container), change the `host` in `dbt/profiles.yml` from `postgres` to `localhost` (the compose file maps port 5432) or keep using the container.

## Repo-specific conventions and patterns

- dbt project: `dbt/my_project/dbt_project.yml` uses `models/example/` with a default materialization of `view` (see the `models:` block). Individual SQL models override that with `{{ config(materialized='table') }}` as needed (see `models/example/my_first_dbt_model.sql`).
- Tests: model-level tests are declared in `models/example/schema.yml` (e.g., `unique`, `not_null`). Run them with `dbt test` as shown above.
- Artifacts: after dbt runs, inspect `dbt/target/manifest.json` and `dbt/target/run_results.json` for programmatic metadata used by downstream tools or CI.

## Important files to reference

- `docker-compose.yml` — service definitions and port mappings (Airflow webserver on 8080, Postgres 5432).
- `dbt/profiles.yml` — connection details; intended to be used from inside the `dbt` container (host=postgres).
- `dbt/my_project/dbt_project.yml` — dbt project configuration (model paths, default materializations).
- `dbt/my_project/models/example/` — concrete model examples (materialization, schema tests).

## When editing or adding DAGs / dbt runs

- Add DAG Python files under `dags/` — they will be picked up automatically by the Airflow container when it runs (because `./dags` is mounted).
- If you want Airflow to execute dbt inside the `dbt` container, call the same `docker-compose run --rm dbt ...` commands from your task/operator. Keep the `--profiles-dir .` flag so dbt can read `dbt/profiles.yml` mounted at `/usr/app`.

## Examples to show common patterns

- Example: model overrides materialization in SQL (see `dbt/my_project/models/example/my_first_dbt_model.sql`):

  - Uses `{{ config(materialized='table') }}` to force a table for the model despite the top-level config.

- Example: test config is declared in YAML (see `dbt/my_project/models/example/schema.yml`) and executed with `dbt test`.

## Useful follow-ups (ask me to add)

- Add a small example DAG that triggers `docker-compose run --rm dbt dbt run --profiles-dir .` so maintainers have a working end-to-end example.
- Add a Makefile or npm task with the common commands (`up`, `dbt:run`, `dbt:test`) if you want simpler local developer UX.

If any section is unclear or you want more detail (for example, an example Airflow operator/task that runs dbt inside the container), tell me which part to expand and I’ll iterate.
