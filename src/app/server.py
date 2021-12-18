import uvicorn

from utils.log import get_uvicorn_config

from .main import app


def run_server(port: int):
    uvicorn.run(app, host="0.0.0.0", port=port, log_config=get_uvicorn_config())
