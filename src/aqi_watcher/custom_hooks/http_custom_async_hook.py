from typing import Any, List, Dict
from airflow.hooks.base import BaseHook
import asyncio
import aiohttp
from airflow.models import Connection


class HttpCustomAsyncHook(BaseHook):
    def __init__(
            self, batch_req: List[Any] | Dict, conn_obj: Connection, req_info: List[Dict], api_req_depend: bool = True,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._conn_obj = conn_obj
        self._batch_req = batch_req
        self._req_info = req_info
        self._api_req_depend = api_req_depend
        self.get_conn()

    def get_conn(self) -> Connection:
        conn = self.get_connection(self._conn_obj.conn_id)
        return conn

    @staticmethod
    async def fetch(session, request_obj):
        async with session.request(method=request_obj.method, url=request_obj.url, headers=request_obj.headers) as res:
            return await res.json()

    async def main(self):
        async with aiohttp.ClientSession() as session:
            if self._api_req_depend:
                results: List[Any] = []
                for request in self._batch_req:
                    results.append(await self.fetch(session=session, request_obj=request))
