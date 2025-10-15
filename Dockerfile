FROM apache/airflow:3.1.0

USER airflow
ADD requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

