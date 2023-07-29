from fastapi import Depends, status, Response
from typing import Any

from app.utils import AppModel
from ..models import Word
from datetime import datetime
from pydantic import Field

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class AddWordRequest(AppModel):
    word: str

class GetWordResponse(AppModel):
    id: Any = Field(alias="_id")
    word: Word

@router.post("/users/words", status_code=status.HTTP_201_CREATED)
def add_word(
    input: AddWordRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    timestamp = datetime.now()
    word = Word(word=input.word, timestamp=timestamp)
    word_added = svc.word_repository.add_new_word(jwt_data.user_id, word)
    return GetWordResponse(word=word_added, id=word_added["_id"])
