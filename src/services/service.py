import abc

from . import constants as const
from . import results


class Service(abc.ABC):
    def __init__(self, auth: str) -> None:
        self._auth = auth

    @abc.abstractmethod
    def search_tracks(self, query: str, offset: int = 0) -> results.Tracks:
        pass


def get(service_name: str, **kwargs) -> Service:
    from .spotify import SpotifyApi

    services = {const.ServiceName.SPOTIFY: SpotifyApi}

    return services[service_name](**kwargs)
