import abc

from . import constants as const
from . import results


class Service(abc.ABC):
    def __init__(self, auth: str) -> None:
        self._auth = auth

    @abc.abstractmethod
    def search_tracks(self, query: str, offset: int = 0) -> results.Tracks:
        pass

    @abc.abstractmethod
    def get_track(self, track_id: str) -> results.Audio:
        pass


def get(service_name: str, **kwargs) -> Service:
    from .spotify import SpotifyApi
    from .yandex_music import YandexMusicApi

    services = {
        const.ServiceName.SPOTIFY: SpotifyApi,
        const.ServiceName.YANDEX_MUSIC: YandexMusicApi,
    }

    return services[service_name](**kwargs)
