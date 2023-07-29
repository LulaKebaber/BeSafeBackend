from datetime import datetime
from typing import Optional, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult
from ..models import Contact
from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "username": user["username"],
            "name": user["name"],
            "phone": user["phone"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_username(self, username: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "username": username,
            }
        )
        return user

    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )

class WordsRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_new_word(self, user_id: str, word: str):
        word_id = ObjectId()
        word_data = {
            "_id": word_id,
            "word": word.word,
            "timestamp": word.timestamp,
        }
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={"$push": {"words": word_data}},
        )
        return word_data

    def get_user_words(self, user_id: str):
        user = self.database["users"].find_one({"_id": ObjectId(user_id)}, {"words": 1})
        words = user.get("words", []) if user else []

        return words

    def add_new_contact(self, user_id: str, data: dict):
        contact_id = ObjectId() 
        contact_data = {
            "_id": contact_id,
            "name": data["name"],
            "phone": data["phone"],
            "gps": data["gps"],
        }

        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={"$push": {"contacts": contact_data}},
        )
        return contact_data
    
    def update_contact(self, user_id: str, contact_id: str, data: dict) -> UpdateResult:
        update_data = {
                "contacts.$.name": data["name"],
                "contacts.$.phone": data["phone"],
                "contacts.$.gps": data["gps"],
            }
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id), "contacts._id": ObjectId(contact_id)},
            update={"$set": update_data},
            )

    def get_user_contacts(self, user_id: str) -> List[Contact]:
        user = self.database["users"].find_one(
            {"_id": ObjectId(user_id)}, {"contacts": 1}
        )
        contacts = user.get("contacts", []) if user else []

        return contacts

    def delete_shanyrak_by_id(self, word_id: str, user_id: str) -> DeleteResult:
        return self.database["users"].delete_one(
            {"_id": ObjectId(word_id), "user_id": ObjectId(user_id)}
        )

class TranscriptionRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_new_transcription(self, user_id: str, transcription: str):
        transcription_data = {
            "transcription": transcription.transcription,
            "timestamp": transcription.timestamp,
        }
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={"$push": {"transcriptions": transcription_data}},
        )
