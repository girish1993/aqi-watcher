from typing import Dict, List

from airflow.models import Connection
import pendulum
from airflow.decorators import dag, task
from connectors.http_connector import HttpConnector
from util.config_parser import parse_config


@dag(dag_id="data_ex_1", start_date=pendulum.now(), schedule="@daily", catchup=False)
def perform_data_extraction():
    @task
    def setup_env() -> Dict:
        try:
            return parse_config()
        except Exception as e:
            print(e)

    @task
    def get_or_create_conn(config: Dict) -> List[Connection]:
        connections: List[HttpConnector] = [
            HttpConnector(
                conn_id=config_item.get("connection"),
                conn_type="http",
                host=config_item.get("host"),
                description=config_item.get("description"),
            )
            for config_item in config.get("apis")
        ]

        return [
            connection.create_connection_if_not_exists() for connection in connections
        ]

    config = setup_env()
    print("config", config)
    connection = get_or_create_conn(config)
    print(connection)


perform_data_extraction()
