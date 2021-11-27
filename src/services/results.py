import typing
from dataclasses import dataclass


@dataclass
class Artist:
    name: str


@dataclass
class Track:
    name: str
    artist: Artist
    image_url: str
    duration: int


Tracks: typing.TypeAlias = list[Track]
