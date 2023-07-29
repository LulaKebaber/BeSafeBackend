from fastapi import Depends, status, Response
from typing import Any

from app.utils import AppModel
from pydantic import Field

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from ..models import Contact


class AddContactRequest(AppModel):
    name: str
    phone: str
    gps: bool

class GetContactsResponse(AppModel):
    id: Any = Field(alias="_id")
    name: str
    phone: str
    gps: bool

@router.post("/users/contacts", status_code=status.HTTP_201_CREATED)
def add_contact(
    input: AddContactRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    contact = svc.word_repository.add_new_contact(jwt_data.user_id, input.dict())
    return GetContactsResponse(name=contact["name"], phone=contact["phone"], gps=contact["gps"], id=contact["_id"])
