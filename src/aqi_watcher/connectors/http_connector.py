from typing import Optional

from airflow import settings
from airflow.models import Connection
from airflow.settings import Session


class HttpConnector(Connection):
    def __init__(
            self,
            conn_id: str,
            conn_type: str,
            host: str,
            description: Optional[str] = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.conn_type = conn_type
        self.description = description
        self.host = host

    def _get_connection(self) -> Connection | None:
        conn: Connection = super().get_connection_from_secrets(self.conn_id)
        if conn:
            return conn
        return None

    def create_connection_if_not_exists(self) -> Connection:
        if self._get_connection() is not None:
            conn = super().__init__(self)
            session: Session = settings.Session()
            session.add(conn)
            session.commit()
            return conn
        return self._get_connection()
