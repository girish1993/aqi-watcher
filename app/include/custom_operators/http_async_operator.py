import asyncio
from typing import Any, List, Dict

import multidict
from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from include.models.request_model import RequestModel
from include.custom_hooks.http_custom_async_hook import HttpCustomAsyncHook


class HttpAsyncOperator(BaseOperator):
    def __init__(self, conn_obj: Dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn_obj = conn_obj
        self._http_async_hook = None

    def execute(self, context: Context = None) -> Any:
        batch_requests: List[RequestModel] = self._setup_requests()
        self._http_async_hook: HttpCustomAsyncHook = HttpCustomAsyncHook(
            batch_req=batch_requests, conn_obj=self.conn_obj, api_req_depend=False
        )
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._http_async_hook.main())

    def _setup_requests(self) -> List[RequestModel]:
        batch_requests = []
        headers = {
            "content-type": "application/json",
            "X-API-Key": self.conn_obj.get("api_key"),
        }
        for endpoint in self.conn_obj.get("endpoints"):
            method = endpoint.get("method")
            params = multidict.MultiDict(endpoint.get("params"))
            url = f"{self.conn_obj.get('host')}{endpoint.get('route')}"
            batch_requests.append(
                RequestModel(method=method, url=url, params=params, headers=headers)
            )
        return batch_requests
