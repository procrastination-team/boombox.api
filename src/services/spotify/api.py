import functools
from http import HTTPStatus

import spotipy

from utils.log import logger

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
                    msg_warn = "Unauthorized access to spotify api"
                    logger.warning(msg_warn)

                    exc_info = exc.msg.split("\n")[-1].strip()
                    raise err.BadTokenError(exc_info)
                case _:
                    msg_err = "Error from spotify api"
                    logger.error(msg_err, exc_info=True)

                    raise err.ServiceError(msg_err)
        except Exception:
            msg_err = "Unhandled error"
            logger.error(msg_err, exc_info=True)

            raise err.ServiceError(msg_err)

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
                id=track["id"],
                name=track["name"],
                artists=results.Artists(
                    [
                        results.Artist(name=artist["name"])
                        for artist in track["artists"]
                    ]
                ),
                image_url=track["album"]["images"][0]["url"],
                duration=track["duration_ms"],
            )
            for track in tracks
        ]

    def get_track(self, track_id: str) -> results.Audio:
        raise err.BadRequestError("Should use SDK")
