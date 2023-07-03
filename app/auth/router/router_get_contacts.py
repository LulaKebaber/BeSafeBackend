from typing import List

from fastapi import Depends, status

from app.utils import AppModel

from ..models import Contact

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class GetAllContactsResponse(AppModel):
    contacts: List[Contact]


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
    return GetAllContactsResponse(contacts=contacts)
