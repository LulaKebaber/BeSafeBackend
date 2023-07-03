from fastapi import Depends, HTTPException, status, Response

from app.utils import AppModel

from ...adapters.jwt_service import JWTData
from ...service import Service, get_service
from .. import router
from ..dependencies import parse_jwt_user_data


class AddWordRequest(AppModel):
    email: str
    password: str


@router.post("/users/{user_id}/words", status_code=status.HTTP_201_CREATED)
def register_user(
    input: AddWordRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    svc.word_repository.add_new_word(jwt_data.user_id, input)
    return Response(status_code=200)
