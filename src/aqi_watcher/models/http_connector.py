from airflow import settings
from airflow.models import Connection
from dotenv import dotenv_values
import os

config = dotenv_values(os.path.join("src/aqi_watcher", ".env"))


def create_connection():
    http_conn = Connection(
        conn_id="aqi_http_conn", conn_type="http", host=config["HTTP_API_HOST"]
    )

    with settings.Session() as sesh:
        sesh.add(http_conn)
        sesh.commit()
