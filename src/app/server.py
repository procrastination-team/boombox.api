import uvicorn

from .main import app


def run_server(port: int):
    uvicorn.run(app, host="0.0.0.0", port=port)
