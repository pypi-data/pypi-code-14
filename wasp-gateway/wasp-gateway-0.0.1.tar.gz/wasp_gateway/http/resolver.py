from abc import ABCMeta
from abc import abstractmethod

from typing import Dict, Optional


class ServiceResolver(metaclass=ABCMeta):
    """
    A service resolver matches a service name to a url.

    TODO: perhaps this need to encourage context manager
          behavior since some strategies could be based
          on leases.
    """
    @abstractmethod
    async def resolve(self, service) -> Optional[str]:
        """Resolve an IP for a service by name.
        This is expected to have been load balanced."""


class DictServiceResolver(ServiceResolver):
    """
    Simple in-memory resolver using a dictionary as the
    storage unit. Only supports 1 mapping per service
    for the initial, dumb impl.
    """
    def __init__(self, services: Dict[str, str]):
        self._services = services

    async def resolve(self, service: str) -> str:
        return self._services.get(service)
