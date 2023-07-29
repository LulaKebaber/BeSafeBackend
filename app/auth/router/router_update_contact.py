from fastapi import Depends, status, HTTPException
from app.utils import AppModel
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data
from bson.objectid import ObjectId


class UpdateContactRequest(AppModel):
    name: str
    phone: str
    gps: bool


@router.put("/users/contacts/{contact_id}", status_code=status.HTTP_200_OK)
def update_contact(
    contact_id: str,
    input: UpdateContactRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    contact_updated = svc.words_repository.update_contact(jwt_data.user_id, contact_id, input.dict())
    
    return {"detail": "Contact updated successfully"}
