from fastapi import Depends, status, File, UploadFile, HTTPException, FastAPI
from ..models import Transcription
from datetime import datetime
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service, check_words_in_text
from . import router
from .dependencies import parse_jwt_user_data

import requests

@router.post("/users/transcriptions", status_code=status.HTTP_201_CREATED)
def transcribe_audio(
    file: UploadFile = File(...),
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    # Make sure we're at the start of the file
    file.file.seek(0)

    # Transcribe the audio file using OpenAI's Whisper ASR API
    response = requests.post(
        "https://api.openai.com/v1/audio/transcriptions",
        headers={
            "Authorization": "Bearer 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",
        },
        files={"file": (file.filename, file.file)},  # Corrected here
        data={"model": "whisper-1"},
    )

    # Check the status of the request
    if response.status_code != 200:
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.json()}")
        raise HTTPException(status_code=400, detail="Transcription failed")

    # Get the transcription from the response
    data = response.json()

    # Create a new Transcription object and save it to the database
    timestamp = datetime.now()
    transcription = data["text"]
    transcription = Transcription(transcription=transcription, timestamp=timestamp)
    svc.transcription_repository.add_new_transcription(jwt_data.user_id, transcription)

    words = svc.word_repository.get_user_words(user_id=jwt_data.user_id)
    array_of_words = [word["word"] for word in words]

    if check_words_in_text(array_of_words, data["text"]):
        svc.repository.threat_recognised(jwt_data.user_id)
        return True
    return False