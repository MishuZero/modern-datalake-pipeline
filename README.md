# Modern Datalake Pipeline (Airflow + MinIO + Iceberg + Nessie + Dremio)

A modern, containerized data-lakehouse pipeline that demonstrates **ingestion**, **storage**, **catalog/versioning**, and **query** layers using open-source tooling. The project uses **Apache Airflow** for orchestration, **MinIO** as S3-compatible storage, **Apache Iceberg** for table format, **Project Nessie** for catalog/version control, and **Dremio** for analytics queries.

## Why this is a hireable Data Engineering project
This repository demonstrates core data engineering skills that are relevant to production pipelines:

- **Orchestration & automation**: Airflow DAGs define repeatable, scheduled pipelines and task dependencies.
- **Data generation & ingestion**: A DAG creates synthetic customer/transaction data, writes to CSV, and uploads to object storage (MinIO).
- **Lakehouse fundamentals**: The architecture is designed around Iceberg + Nessie to support schema evolution, ACID-like semantics, and table versioning.
- **Containerized environments**: Docker Compose provides reproducibility for the entire stack, making it easy to demo and iterate.

## Architecture overview
| Component | Role |
| --- | --- |
| **Apache Airflow** | Orchestrates ingestion and transformation tasks |
| **MinIO (S3)** | Stores raw and processed data |
| **Apache Iceberg** | Table format for analytics-ready storage |
| **Project Nessie** | Catalog + version control for Iceberg tables |
| **Dremio** | Query engine for SQL analytics |
| **Docker Compose** | Runs the stack locally |

## Data flow
1. **Ingestion** — Airflow generates synthetic banking data and saves CSV files locally.
2. **Storage** — Airflow uploads CSVs to MinIO buckets.
3. **Cataloging/Versioning** — Iceberg + Nessie manage table metadata (as you expand transformations).
4. **Querying** — Dremio can query Iceberg tables via Nessie.

## Usability expectations
This project is intended for **local development and demos**. When using it, expect:

- **Local resources required**: Docker + Docker Compose are required to run the stack.
- **Synthetic data**: The DAGs generate fake data for demonstration and are not tied to a production data source.
- **Manual setup steps**: You’ll need to configure connections in Airflow/Dremio if you want to query the data end-to-end.
- **Extensibility**: The repository is a scaffold; you can add transformations, Iceberg table creation, and Nessie branching/tagging workflows.

## Getting started
### 1) Start the stack
```bash
docker-compose up -d
```

### 2) Airflow DAGs
- `bank_transaction_pipeline` (test DAG)
- `generate_banking_data_to_minio` (creates + uploads synthetic banking data)

### 3) Next steps (optional)
- Add Iceberg table creation and data transformations.
- Configure Dremio to query Iceberg tables via Nessie.
- Add CI checks and data quality validations.

## Repository layout
```
.
├── dags/
│   ├── Airflow_dag_test.py
│   └── Bank_Data_Dag.py
├── docker-compose.yaml
├── requirements.txt
└── pyproject.toml
```

## Notes
- Default MinIO credentials are set in the DAG; update for production usage.
- The DAGs write temporary files to `/tmp` inside the Airflow container.

---
Author: Rakibul Hasan (MishuZero)
GitHub: @MishuZero
