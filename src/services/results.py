import typing
from dataclasses import dataclass


@dataclass
class Artist:
    name: str


Artists = typing.TypeAlias = list[Artist]


@dataclass
class Track:
    id: str
    name: str
    artists: Artists
    image_url: str
    duration: int


Tracks: typing.TypeAlias = list[Track]
