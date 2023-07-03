from typing import Any

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class GetAllWordsResponse(AppModel):
    words: dict


@router.get("/users/words", response_model=GetAllWordsResponse)
def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    words = svc.word_repository.get_user_words(jwt_data.user_id)
    return words
