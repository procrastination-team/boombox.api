import functools

import applemusicpy

from utils.log import logger

from .. import Service
from .. import errors as err
from .. import results


def _handle_api_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            msg_err = "Unhandled error"
            logger.error(msg_err, exc_info=True)

            raise err.ServiceError(msg_err)

    return wrapper


class AppleMusicApi(Service):
    def __init__(self, auth: str) -> None:
        super().__init__(auth)
        self.__client = applemusicpy.AppleMusic(self._auth, "kek", "lol")

    @_handle_api_error
    def search_tracks(self, query: str, offset: int = 0) -> results.Tracks:
        response = self.__client.search(query, offset=offset, types=["songs"])
        songs = response["results"]["songs"]["data"]

        image_size = {"w": 400, "h": 400}
        return [
            results.Track(
                id=song["id"],
                name=song["attributes"]["name"],
                artists=results.Artists(
                    [results.Artist(name=song["attributes"]["artistName"])]
                ),
                image_url=song["attributes"]["artwork"]["url"].format(**image_size),
                duration=song["attributes"]["durationInMillis"],
            )
            for song in songs
        ]

    def get_track(self, track_id: str) -> results.Audio:
        raise err.BadRequestError("Should use SDK")
