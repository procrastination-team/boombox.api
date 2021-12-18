import logging

_LEVEL = "DEBUG"
_FORMAT = '[%(asctime)s] [%(levelname)s] "%(message)s"'
_REQUEST_FORMAT = (
    '[%(asctime)s] [%(levelname)s] %(client_addr)s - "%(request_line)s" %(status_code)s'
)
_DATE_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


def _create_logger() -> logging.Logger:
    fmt = logging.Formatter(_FORMAT, _DATE_FORMAT)

    hdlr = logging.StreamHandler()
    hdlr.setFormatter(fmt)

    root = logging.getLogger()
    root.addHandler(hdlr)

    logger = logging.getLogger(__name__)
    logger.setLevel(_LEVEL)
    return logger


logger = _create_logger()


def get_uvicorn_config() -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": _FORMAT,
                "datefmt": _DATE_FORMAT,
                "use_colors": False,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": _REQUEST_FORMAT,
                "datefmt": _DATE_FORMAT,
                "use_colors": False,
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "class": "logging.StreamHandler",
                "formatter": "access",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "uvicorn": {
                "level": _LEVEL,
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": _LEVEL,
            },
            "uvicorn.access": {
                "level": _LEVEL,
                "handlers": ["access"],
                "propagate": False,
            },
        },
    }
