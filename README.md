## 🏗️ Modern Datalake House ELT Pipeline

This project demonstrates a **modern data lakehouse architecture** built using **open-source technologies** — designed for scalability, version control, and analytics.

---

## 🧩 Architecture Overview

### 🔧 Components
| Component | Role |
|------------|------|
| **Apache Airflow** | Orchestrates ETL — ingestion, validation, transformation |
| **MinIO (S3 Storage)** | Stores raw and processed data |
| **Apache Iceberg** | Manages structured, versioned tables in the data lake |
| **Project Nessie** | Acts as the catalog and version control for Iceberg tables |
| **Dremio** | Executes SQL queries directly on Iceberg tables |
| **Docker** | Runs all components in isolated, reproducible containers |

---


<img width="800" height="953" alt="System Design" src="https://github.com/user-attachments/assets/5c8e7571-d601-45c2-86e2-b0c697c7ac38" />

## ⚙️ Data Flow
1. **Ingestion** — Airflow pulls data from sources (DBs, APIs, CSVs).  
2. **Transformation** — Airflow processes and writes Iceberg tables.  
3. **Storage** — Data resides in MinIO (S3-compatible).  
4. **Cataloging** — Nessie tracks Iceberg tables, metadata, and versions.  
5. **Querying** — Dremio queries Iceberg tables using Nessie as the catalog.  

---

## 🪶 Versioning Strategy
- **Code Version:** Managed via Git & GitHub (`git tag v1.0.0`)  
- **Data Version:** Managed by Project Nessie (`TAG v1.0.0 IN nessie`)  

---

## 🚀 Deployment
To start all services using Docker Compose:
```bash
docker-compose up -d

Rakibul Hasan (MishuZero)
GitHub: @MishuZero
```
