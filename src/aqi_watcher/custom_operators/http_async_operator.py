from typing import Any

from airflow.models.baseoperator import BaseOperator
import asyncio
import aiohttp
from airflow.utils.context import Context


class HttpAsyncOperator(BaseOperator):
    def execute(self, context: Context) -> Any:
        pass
