# 🚀 End-to-End ML Pipeline with Apache Airflow & Docker

This project demonstrates an end-to-end **machine learning pipeline** built with **Apache Airflow** and **Docker**.
The pipeline automates steps like data ingestion, preprocessing, model training, experiment tracking, and saving results.

---

## ⚡ Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Shuv13/Containerized-ML-Workflow-Orchestrator.git
    cd ML
    ```

2.  **(Optional) Create and activate a virtual environment**
    ```bash
    # macOS/Linux
    python -m venv venv
    source venv/bin/activate  
    
    # Windows
    python -m venv venv
    venv\Scripts\activate   
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start Airflow and PostgreSQL with Docker**
    ```bash
    docker compose up -d
    ```

5.  **🔗 Configure Airflow Connection**
    
    Airflow needs a connection to the PostgreSQL database used for tracking experiments and saving batch data.
    
    Run this command to add the connection inside the Airflow container:
    
    ```bash
    docker compose run --rm airflow-cli bash -lc \
    "airflow connections add 'postgres_default' \
    --conn-uri 'postgresql+psycopg2://airflow:airflow@postgres:5432/airflow'"
    ```
    *If the connection already exists, you can ignore the warning.*

## ▶️ Usage

1.  **Open the Airflow UI:**
    [http://localhost:8080](http://localhost:8080)

2.  **Login with the default credentials:**
    * **Username:** `airflow`
    * **Password:** `airflow`

3.  **In the Airflow UI:**
    * Locate the DAG called `ml_pipeline`
    * Enable it (toggle switch on the left)
    * Trigger it manually (play button on the right) or wait for the daily schedule (`@daily`)

4.  Check task logs in the UI if anything fails.

## 🛑 Stop Services

To stop all running services:
```bash
docker compose down
```

## 📌 Notes

* The project uses PostgreSQL as a backend database for Airflow and for experiment tracking.
* The container may install extra libraries (like scikit-learn) when starting. This is fine for development but not recommended for production.
* For production usage, you should build a custom Docker image with all dependencies baked in. See Airflow’s docs.

## 📚 References

* Apache Airflow Documentation
