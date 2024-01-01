from typing import Dict

from airflow.models import Connection
import pendulum
from airflow.decorators import dag, task
from app.plugins.connectors.http_connector import HttpConnector
from pyconfigparser import configparser


@dag(dag_id="data_ex_1", start_date=pendulum.now(), schedule="@daily", catchup=False)
def perform_data_extraction():
    @task
    def setup_env(config_dir: str, file_name: str) -> Dict:
        try:
            return configparser.get_config(
                config_dir=config_dir, file_name=file_name
            )
        except Exception as e:
            print(e)

    @task
    def get_or_create_conn(config: Dict) -> Connection:
        http_connector: HttpConnector = HttpConnector(conn_id=config.apis.connection, conn_type="http",
                                                      host=config.apis.host,
                                                      description=config.apis.description)
        return http_connector.create_connection_if_not_exists()

    config = setup_env(config_dir="app/config", file_name="config.yaml")
    connection = get_or_create_conn(config)


perform_data_extraction()
