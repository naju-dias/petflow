FROM apache/airflow:2.8.1

USER airflow

RUN pip install --no-cache-dir "typing_extensions>=4.8.0"