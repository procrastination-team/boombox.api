import functools

import yandex_music
import yandex_music.exceptions

from utils.log import logger

from .. import Service
from .. import errors as err
from .. import results


def _handle_api_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except yandex_music.exceptions.Unauthorized as exc:
            msg_warn = f"Unauthorized access to yandex music api. Error: `{exc}`"
            logger.warning(msg_warn)

            exc_info = str(exc)
            raise err.BadTokenError(exc_info)
        except yandex_music.exceptions.YandexMusicError as exc:
            msg_err = f"Error from yandex music api"
            logger.error(msg_err, exc_info=True)

            raise err.ServiceError(msg_err) from exc
        except Exception as exc:
            msg_err = f"Unhandled error"
            logger.error(msg_err, exc_info=True)

            raise err.ServiceError(msg_err) from exc

    return wrapper


class YandexMusicApi(Service):
    def __init__(self, auth: str) -> None:
        super().__init__(auth)
        self.__auth()

    @_handle_api_error
    def __auth(self) -> None:
        msg_info = "Trying to auth into YandexApi"
        logger.info(msg_info)

        self.__client = yandex_music.Client.from_token(self._auth)
        self.__client.logger.propagate = False

    @_handle_api_error
    def search_tracks(self, query: str, offset: int = 0) -> results.Tracks:
        search_result = self.__client.search(query, page=offset, type_="track")
        tracks = search_result["tracks"]["results"]

        image_size = "400x400"
        return [
            results.Track(
                id=str(track["id"]),
                name=track["title"],
                artists=results.Artists(
                    [results.Artist(name=artist["name"]) for artist in track["artists"]]
                ),
                image_url=track["cover_uri"].replace("%%", image_size),
                duration=track["duration_ms"],
            )
            for track in tracks
        ]

    @_handle_api_error
    def get_track(self, track_id: str) -> results.Audio:
        track = self.__client.tracks(track_id)[0]
        tracks_info = track.get_download_info(get_direct_links=True)

        for info in tracks_info:
            if info["codec"] == "mp3":
                track_link = info["direct_link"]
                break

        content = self.__client.request.retrieve(track_link).content

        return results.Audio(content)
