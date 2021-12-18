from .api import YandexMusicApi

__all__ = ("YandexMusicApi",)


def _disable_logs():
    import yandex_music.base

    yandex_music.base.logger.setLevel("ERROR")


_disable_logs()
