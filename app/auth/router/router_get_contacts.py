from typing import List, Dict, Any

from fastapi import Depends, status

from app.utils import AppModel

from ..models import Contact

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data

class GetUsernameResponse(AppModel):
    _id: str
    username: str
    name: str
    phone: str

class GetAllContactsResponse(AppModel):
    contacts: List[Dict[str, Any]]

@router.get(
    "/users/contacts",
    response_model=GetAllContactsResponse,
    status_code=status.HTTP_200_OK,
)
def get_contacts(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> GetAllContactsResponse:
    contacts = svc.word_repository.get_user_contacts(jwt_data.user_id)
    users = []

    for contact in contacts:
        user = svc.repository.get_user_by_username(username=contact["username"])
        users.append(GetUsernameResponse(
                _id=user["_id"],
                username=user["username"],
                name=user["name"],
                phone=user["phone"]
            ))
    return GetAllContactsResponse(contacts=users)

    
