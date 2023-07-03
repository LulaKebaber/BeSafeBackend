from typing import List, Dict, Any

from fastapi import Depends

from app.utils import AppModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class GetAllWordsResponse(AppModel):
    words: List[Dict[str, Any]]


@router.get("/users/words", response_model=GetAllWordsResponse)
def get_user_words(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> GetAllWordsResponse:
    words_with_timestamps = svc.word_repository.get_user_words(jwt_data.user_id)
    return GetAllWordsResponse(words=words_with_timestamps)
