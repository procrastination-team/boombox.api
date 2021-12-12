from io import BytesIO
from typing import Iterator

import services


def stream_audio(audio: services.results.Audio) -> Iterator[bytes]:
    yield from BytesIO(audio.content)
