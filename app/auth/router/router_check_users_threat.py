from fastapi import Depends, status, File, UploadFile, HTTPException, FastAPI
from ..models import Transcription
from datetime import datetime
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service, check_words_in_text
from . import router
from .dependencies import parse_jwt_user_data

@router.post("/users/contacts", status_code=status.HTTP_201_CREATED)
def check_for_threat(
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    contacts = svc.word_repository.get_user_contacts(user_id=jwt_data.user_id)

    for contact in contacts:
        user = svc.repository.get_user_by_username(username=contact["username"])

        if user["threat_recognised"]:
            return user["username"]
    
    
    
        # contacts = svc.word_repository.get_user_contacts(jwt_data.user_id)
        # for contact in contacts:
        #     # Предположим, что поле `username` указывает на имя пользователя для каждого контакта
        #     # и что это уникальное значение для каждого пользователя
        #     contact_username = contact["username"]
        #     user = svc.repository.get_user_by_username(username=contact_username)
        #     if user["threat_recognised"] == True:
        #         return 