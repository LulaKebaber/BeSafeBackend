from typing import List

from fastapi import Depends
from pydantic import Field

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class Word(AppModel):
    word: str


class GetAllWordsResponse(AppModel):
    words: List[Word]


@router.get("/users/words", response_model=GetAllWordsResponse)
def get_user_words(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> GetAllWordsResponse:
    words = svc.word_repository.get_user_words(jwt_data.user_id)
    return GetAllWordsResponse(words=[Word(word=w) for w in words])
