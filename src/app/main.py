from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import services
from utils.log import logger

from .helpers import stream_audio

app = FastAPI()
bearer = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/{service_name}/search/", response_model=services.results.Tracks)
def search_tracks(
    service_name: services.ServiceName,
    q: str,
    offset: int = 0,
    auth_credentials: HTTPAuthorizationCredentials = Depends(bearer),
):
    try:
        service = services.get(service_name, auth=auth_credentials.credentials)

        msg_info = f"Searching tracks for {service_name}"
        logger.info(msg_info)

        tracks = service.search_tracks(q, offset)
    except services.BadTokenError as exc:
        msg_err = str(exc)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg_err)
    except services.BadRequestError as exc:
        msg_err = str(exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg_err)
    except services.ServiceError as exc:
        msg_err = str(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg_err
        )

    return tracks


@app.get("/api/v1/{service_name}/track/", response_class=StreamingResponse)
def get_track(
    service_name: services.ServiceName,
    track_id: str,
    auth_credentials: HTTPAuthorizationCredentials = Depends(bearer),
):
    try:
        service = services.get(service_name, auth=auth_credentials.credentials)

        msg_info = f"Downloading track for {service_name}"
        logger.info(msg_info)

        audio = service.get_track(track_id)
    except services.BadTokenError as exc:
        msg_err = str(exc)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg_err)
    except services.BadRequestError as exc:
        msg_err = str(exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg_err)
    except services.ServiceError as exc:
        msg_err = str(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg_err
        )

    return StreamingResponse(stream_audio(audio), media_type="audio/mpeg")
