from fastapi import Depends, status, File, UploadFile
from ..models import Transcription
from datetime import datetime
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data

from openai import OpenAI
from openai.api_resources import Audio

# Create an instance of the OpenAI client
openai = OpenAI("your_openai_api_key")

@router.post("/users/transcriptions", status_code=status.HTTP_201_CREATED)
def transcribe_audio(
    file: UploadFile = File(...),
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    # Transcribe the audio file using OpenAI's Whisper ASR API
    audio = Audio.create(openai, file=file.file.read(), model="whisper-1")
    transcription = audio['transcription']

    # Create a new Transcription object and save it to the database
    timestamp = datetime.now()
    transcription = Transcription(transcription=transcription, timestamp=timestamp)
    svc.transcription_repository.add_new_transcription(jwt_data.user_id, transcription)

    return {'status': 'success', 'transcription': transcription}
