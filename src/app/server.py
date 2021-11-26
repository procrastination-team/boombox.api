import uvicorn

from .main import app


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8888)
