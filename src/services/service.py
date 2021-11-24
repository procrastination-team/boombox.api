import abc

from . import constants as const
from . import results


class Service(abc.ABC):
    @abc.abstractmethod
    def search_tracks(self, query: str, offset: int = 0) -> results.Tracks:
        pass


def get(service_name: str, **kwargs) -> Service:
    from .spotify import SpotifyApi

    services = {const.ServiceName.SPOTIFY: SpotifyApi}

    return services[service_name](**kwargs)
