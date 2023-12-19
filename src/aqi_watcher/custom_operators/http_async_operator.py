import asyncio
from typing import Any, List

import multidict
from airflow.models import Connection
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from pyconfigparser import configparser

from src.aqi_watcher.models.request_model import RequestModel
from src.aqi_watcher.custom_hooks.http_custom_async_hook import HttpCustomAsyncHook
from src.aqi_watcher.connectors.http_connector import HttpConnector


class HttpAsyncOperator(BaseOperator):
    def __init__(self, conn_obj: Connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn_obj = conn_obj
        self._config_requests = None
        self._http_async_hook = None

    def execute(self, context: Context) -> Any:
        # parse config
        self.parse_requests_config()

        # setup connection if not exists
        http_connector: HttpConnector = HttpConnector(conn_id=self._config_requests.apis.connection, conn_type="http",
                                                      host=self._config_requests.apis.host,
                                                      description=self._config_requests.apis.description)
        conn: Connection = http_connector.create_connection_if_not_exists()

        # prepare requests
        batch_requests: List[RequestModel] = self.setup_requests()
        http_async_hook: HttpCustomAsyncHook = HttpCustomAsyncHook(
            batch_req=batch_requests,
            conn_obj=conn,
            api_req_depend=False
        )

        # create asyncio event loop
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(http_async_hook.main())

    def parse_requests_config(self):
        self._config_requests = configparser.get_config(
            config_dir="src/config", file_name="config.yaml"
        )

    def setup_requests(self):
        batch_requests: List[RequestModel] = []
        for each_api_batch in self._config_requests.apis:
            headers = {
                "content-type": "application/json",
                "X-API-Key": each_api_batch.api_key,
            }
            for endpoint in each_api_batch:
                method = endpoint.method
                params = multidict.MultiDict(endpoint.params)
                url = f"{each_api_batch.host}{endpoint.path}"
                batch_requests.append(
                    RequestModel(method=method, url=url, params=params, headers=headers)
                )
        return batch_requests
