import functools
from http import HTTPStatus

import spotipy

from .. import Service
from .. import errors as err
from .. import results


def _handle_api_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except spotipy.SpotifyException as exc:
            match exc.http_status:
                case HTTPStatus.UNAUTHORIZED:
                    exc_info = exc.msg.split("\n")[-1].strip()
                    raise err.BadTokenError(exc_info)
                case _:
                    msg_err = "Error from spotify api"
                    raise err.ServiceError(msg_err) from exc
        except Exception as exc:
            msg_err = "Unhandled error"
            raise err.ServiceError(msg_err) from exc

    return wrapper


class SpotifyApi(Service):
    def __init__(self, auth: str) -> None:
        super().__init__(auth)
        self.__client = spotipy.Spotify(auth=self._auth)

    @_handle_api_error
    def search_tracks(self, query: str, offset: int = 0) -> results.Tracks:
        response = self.__client.search(query, offset=offset, type="track")
        tracks = response["tracks"]["items"]
        return [
            results.Track(
                name=track["name"],
                artist=results.Artist(name=track["album"]["artists"][0]["name"]),
                image_url=track["album"]["images"][0]["url"],
                duration=track["duration_ms"],
            )
            for track in tracks
        ]
