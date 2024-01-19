from typing import Dict, List

import pendulum
from airflow.decorators import dag, task
from include.connectors.http_connector import HttpConnector
from include.custom_operators.http_async_operator import HttpAsyncOperator
from include.util.config_parser import parse_config


@dag(dag_id="data_ex_1", start_date=pendulum.now(), schedule="@daily", catchup=False)
def perform_data_extraction():
    @task
    def setup_env() -> Dict:
        try:
            return parse_config()
        except Exception as e:
            print(e)

    @task
    def get_or_create_conn(config: Dict) -> List[Dict]:
        connections: List[HttpConnector] = [
            HttpConnector(
                conn_id=config_item.get("connection"),
                conn_type="http",
                host=config_item.get("host"),
                description=config_item.get("description"),
            )
            for config_item in config.get("apis")
        ]

        [connection.create_connection_if_not_exists() for connection in connections]
        print("set_connections", [connection.serialise() for connection in connections])
        return [connection.serialise() for connection in connections]

    @task
    def make_http_calls(config: Dict):
        opera_1 = HttpAsyncOperator(task_id="http_conn", conn_obj=config)
        print(opera_1)

    config = setup_env()
    set_connections = get_or_create_conn(config)
    # make_http_calls(config=set_connections)


perform_data_extraction()
