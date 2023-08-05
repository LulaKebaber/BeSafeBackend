from fastapi import Depends, status, HTTPException
from typing import Any

from app.utils import AppModel
from pydantic import Field

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data

class AddContactRequest(AppModel):
    username: str
    phone: str
    gps: bool

class GetContactsResponse(AppModel):
    id: Any = Field(alias="_id")
    username: str
    phone: str
    gps: bool

@router.post("/users/contacts", status_code=status.HTTP_201_CREATED)
def add_contact(
    input: AddContactRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    if not svc.repository.get_user_by_username(input.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not found.",
        )
    
    contact = svc.word_repository.add_new_contact(jwt_data.user_id, input.dict())
    return GetContactsResponse(username=contact["username"], phone=contact["phone"], gps=contact["gps"], id=contact["_id"])
    
    # contact = svc.word_repository.add_new_contact(jwt_data.user_id, input.dict())
    # return GetContactsResponse(username=contact["username"], phone=contact["phone"], gps=contact["gps"], id=contact["_id"])
