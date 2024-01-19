from typing import Optional, Dict

from airflow import settings
from airflow.exceptions import AirflowNotFoundException
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

    def serialise(self) -> Dict:
        serialized_dict = self.__dict__.copy()
        serialized_dict.pop('_sa_instance_state', None)
        return serialized_dict

    def _get_connection(self) -> Optional[Connection]:
        try:
            conn: Connection = super().get_connection_from_secrets(self.conn_id)
            return conn
        except AirflowNotFoundException as e:
            return None

    def create_connection_if_not_exists(self) -> None:
        if self._get_connection():
            return self._get_connection()
        conn = Connection(conn_id=self.conn_id, conn_type=self.conn_type, description=self.description,
                          host=self.host)
        session: Session = settings.Session()
        session.add(conn)
        session.commit()
