from typing import Dict, List

import pendulum
from airflow.decorators import dag, task
from include.connectors.http_connector import HttpConnector
from include.custom_operators.http_async_operator import HttpAsyncOperator
from include.util.config_parser import parse_config
from include.dto.response_formulator import DataFactory


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
    def make_http_calls(config_obj: Dict, connections: List[Dict]):
        results: List[Dict] = []
        for i, conn in enumerate(connections):
            res = next(
                (
                    item
                    for item in config_obj.get("apis")
                    if item.get("connection") == conn.get("conn_id")
                ),
                None,
            )
            http_operator = HttpAsyncOperator(task_id=f"{conn.get('connection')}_{i}", conn_obj=res)
            results.append(http_operator.execute())
        return results

    @task
    def format_responses(responses: List[List[Dict]]) -> Dict[str, List[Dict]]:
        return DataFactory.formulate(data=responses)

    config = setup_env()
    set_connections = get_or_create_conn(config)
    api_responses = make_http_calls(config_obj=config, connections=set_connections)
    formatted_responses = format_responses(responses=api_responses)


perform_data_extraction()
