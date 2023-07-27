from app.utils import AppModel
from datetime import datetime


class Contact(AppModel):
    name: str
    phone: str
    gps: bool


class Word(AppModel):
    word: str
    timestamp: datetime

class Transcription(AppModel):
    transcription: str
    timestamp: datetime

