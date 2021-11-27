from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import services

app = FastAPI()
bearer = HTTPBearer()


@app.get("/api/v1/{service_name}/search/", response_model=services.results.Tracks)
def search_tracks(
    service_name: services.ServiceName,
    q: str,
    offset: int = 0,
    auth_credentials: HTTPAuthorizationCredentials = Depends(bearer),
):
    service = services.get(service_name, auth=auth_credentials.credentials)

    try:
        tracks = service.search_tracks(q, offset)
    except services.BadTokenError as exc:
        msg_err = str(exc)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg_err)
    except services.ServiceError as exc:
        msg_err = str(exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg_err
        )

    return tracks
