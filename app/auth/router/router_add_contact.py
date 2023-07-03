from fastapi import Depends, status, Response

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class AddContactRequest(AppModel):
    name: str
    phone: str
    gps: bool


@router.post("/users/contacts", status_code=status.HTTP_201_CREATED)
def add_contact(
    input: AddContactRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    svc.word_repository.add_new_contact(jwt_data.user_id, input.dict())
    return Response(status_code=status.HTTP_201_CREATED)
