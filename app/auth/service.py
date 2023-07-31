from pydantic import BaseSettings

from app.config import database

from .adapters.jwt_service import JwtService
from .repository.repository_auth import AuthRepository
from .repository.repository_auth import WordsRepository
from .repository.repository_auth import TranscriptionRepository


class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800


config = AuthConfig()


class Service:
    def __init__(self):
        self.repository = AuthRepository(database)
        self.word_repository = WordsRepository(database)
        self.transcription_repository = TranscriptionRepository(database)
        self.jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)


def get_service():
    return Service()
