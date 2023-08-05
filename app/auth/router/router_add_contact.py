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

class GetContactsResponse(AppModel):
    id: Any = Field(alias="_id")
    username: str

@router.post("/users/contacts", status_code=status.HTTP_201_CREATED)
def add_contact(
    input: AddContactRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    user = svc.repository.get_user_by_username(input.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not found.",
        )
    contacts = svc.word_repository.get_user_contacts(user_id=jwt_data.user_id)

    for contact in contacts:
        if contact["username"] == user["username"]:
            return "User already added"
        
    
    contact = svc.word_repository.add_new_contact(jwt_data.user_id, user=user)
    return GetContactsResponse(id=contact["_id"], username=contact["username"])
