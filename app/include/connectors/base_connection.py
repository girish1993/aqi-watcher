from __future__ import annotations

from abc import ABC, abstractmethod


class BaseConnection(ABC):

    @abstractmethod
    def _get_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    def serialise(self, *args, **kwargs):
        pass

    @abstractmethod
    def create_connection_if_not_exists(self):
        pass
