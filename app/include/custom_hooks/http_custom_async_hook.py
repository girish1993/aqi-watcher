from typing import List, Dict
from airflow.hooks.base import BaseHook
import asyncio
import aiohttp
from airflow.models import Connection

from include.dto.request_dto import RequestModel


class HttpCustomAsyncHook(BaseHook):
    def __init__(
            self,
            batch_req: List[RequestModel],
            conn_obj: Dict,
            api_req_depend: bool = False,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._conn_obj = conn_obj
        self._batch_req = batch_req
        self._api_req_depend = api_req_depend
        self.get_conn()

    def get_conn(self) -> Connection:
        conn = self.get_connection(self._conn_obj.get("connection"))
        return conn

    @staticmethod
    async def fetch(session, request_obj) -> Dict:
        page: int = 1
        result = []
        while True:
            request_obj.params["page"] = page
            async with session.request(
                    method=request_obj.method,
                    url=request_obj.url,
                    params=request_obj.params,
                    headers=request_obj.headers,
            ) as res:
                page_data = await res.json()
                if page_data.get("results") is not None:
                    result += page_data.get("results")
                    if len(page_data.get("results")) == request_obj.params.get(
                            "limit"):
                        page += 1
                    else:
                        break
                else:
                    break
        return {request_obj.route: result}

    async def main(
            self,
    ):
        async with aiohttp.ClientSession() as session:
            if self._api_req_depend:
                results = []
                for request in self._batch_req:
                    results.append(
                        await self.fetch(session=session, request_obj=request)
                    )
                return results
            else:
                tasks = [
                    asyncio.ensure_future(
                        self.fetch(session=session, request_obj=request)
                    )
                    for request in self._batch_req
                ]
                responses = await asyncio.gather(*tasks)
                return responses
