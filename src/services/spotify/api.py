import spotipy
from spotipy.oauth2 import SpotifyOAuth

from utils import environments as env

from .. import Service, results
from . import structures as struct


class SpotifyApi(Service):
    def __init__(self) -> None:
        credentials = struct.ClientCredentials(
            client_id=env.CLIENT_ID, client_secret=env.CLIENT_SECRET
        )
        self.__client = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope="user-library-read",
                client_id=credentials.client_id,
                client_secret=credentials.client_secret,
                redirect_uri="http://localhost:31337",
            )
        )

    def search_tracks(self, query: str, offset: int = 0) -> results.Tracks:
        response = self.__client.search(query, offset=offset, type="track")
        tracks = response["tracks"]["items"]
        return [
            results.Track(
                name=track["name"],
                url=track["preview_url"],
                artist=results.Artist(name=track["album"]["artists"][0]["name"]),
                image_url=track["album"]["images"][0]["url"],
                duration=track["duration_ms"],
            )
            for track in tracks
        ]
