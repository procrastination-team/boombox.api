from fastapi import FastAPI

import services

app = FastAPI()


@app.get("/api/v1/{service_name}/search/", response_model=services.results.Tracks)
def search_tracks(
    service_name: services.ServiceName,
    q: str,
    offset: int = 0,
):
    service = services.get(service_name)
    tracks = service.search_tracks(q, offset)

    return tracks
