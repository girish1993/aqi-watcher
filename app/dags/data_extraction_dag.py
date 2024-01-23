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
        return [connection.serialise() for connection in connections]

    @task
    def make_http_calls(config: Dict, connections: List[Dict]):
        results: List[Dict] = []
        for i, conn in enumerate(connections):
            res = next(
                (
                    item
                    for item in config.get("apis")
                    if item.get("connection") == conn.get("conn_id")
                ),
                None,
            )
            x = HttpAsyncOperator(task_id=f"{conn.get('connection')}_{i}", conn_obj=res)
            results.append(x.execute())
        return results

    config = setup_env()
    set_connections = get_or_create_conn(config)
    results = make_http_calls(config=config, connections=set_connections)


perform_data_extraction()
