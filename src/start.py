from app import run_server
from utils import environments as env

if __name__ == "__main__":
    run_server(env.SERVICE_PORT)
