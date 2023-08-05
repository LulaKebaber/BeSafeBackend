from fastapi import Depends, status
from app.utils import AppModel
from typing import List, Dict, Any

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data

class GetUsernameResponse(AppModel):
    username: str
    threat_recognised: bool
    latitude: float
    longitude: float

class GetAllContactsResponse(AppModel):
    threats: List[Dict[str, Any]]

@router.get("/users/threats", status_code=status.HTTP_201_CREATED)
def check_for_threat(
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    contacts = svc.word_repository.get_user_contacts(user_id=jwt_data.user_id)
    threat_users = []

    for contact in contacts:
        user = svc.repository.get_user_by_username(username=contact["username"])
        if user["threat_recognised"]:
            threat_users.append( )

    return GetAllContactsResponse(threats=threat_users)
