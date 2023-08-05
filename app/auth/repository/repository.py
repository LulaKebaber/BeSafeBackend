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
            "message": "Please, help me!",
            "latitude": 0,
            "longitude": 0,
            "threat_recognised": False,
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
                "username": username
            }
        )
        return user

    def update_location(self, user_id: str, data: dict) -> UpdateResult:
        return self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                }
            },
        )

    def threat_recognised(self, user_id: str):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "threat_recognised": True,
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
            "timestamp": str(word.timestamp),
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

    def add_new_contact(self, user_id: str, user: dict):
        contact_data = {
            "_id": user["_id"],
            "username": user["username"],
            "phone": user["phone"],
            "name": user["name"],
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
        return self.database["users"].update_one(
            filter={"_id": ObjectId(user_id), "contacts._id": ObjectId(contact_id)},
            update={"$set": update_data},
            )

    def get_user_contacts(self, user_id: str) -> List[Contact]:
        user = self.database["users"].find_one(
            {"_id": ObjectId(user_id)}, {"contacts": 1}
        )
        contacts = user.get("contacts", []) if user else []

        return contacts

    def delete_word_by_id(self, word_id: str, user_id: str) -> DeleteResult:
        return self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"words": {"_id": ObjectId(word_id)}}}
        )
    
    def delete_contact_by_id(self, contact_id: str, user_id: str) -> DeleteResult:
        return self.database["users"].update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"contacts": {"_id": ObjectId(contact_id)}}}
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
