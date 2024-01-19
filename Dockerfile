FROM apache/airflow:2.7.3
RUN pip install poetry==1.6.1
COPY pyproject.toml poetry.lock README.md ./
RUN poetry install
ENV PYTHONPATH "${PYTHONPATH}: /opt/airflow/lib/"