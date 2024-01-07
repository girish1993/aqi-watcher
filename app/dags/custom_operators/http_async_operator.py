import asyncio
from typing import Any, List

import multidict
from airflow.models import Connection
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from ..models.request_model import RequestModel
from ..custom_hooks.http_custom_async_hook import HttpCustomAsyncHook


class HttpAsyncOperator(BaseOperator):
    def __init__(self, conn_obj: Connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn_obj = conn_obj
        self._config_requests = None
        self._http_async_hook = None

    def execute(self, context: Context) -> Any:
        # prepare requests
        batch_requests: List[RequestModel] = self.setup_requests()
        http_async_hook: HttpCustomAsyncHook = HttpCustomAsyncHook(
            batch_req=batch_requests, conn_obj=self.conn_obj, api_req_depend=False
        )

        # create asyncio event loop
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(http_async_hook.main())

    def setup_requests(self):
        batch_requests = []
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
