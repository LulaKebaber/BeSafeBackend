from datetime import datetime
from typing import Optional, List

from bson.objectid import ObjectId
from pymongo.database import Database
from ..router.router_get_contacts import Contact

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
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

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
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
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)}, update={"$push": {"words": word}}
        )

    def get_user_words(self, user_id: str):
        user = self.database["users"].find_one({"_id": ObjectId(user_id)}, {"words": 1})
        words = user.get("words", []) if user else []
        return words

    def add_new_contact(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$push": {
                    "name": data["name"],
                    "phone": data["phone"],
                    "gps": data["gps"],
                }
            },
        )

    def get_user_contacts(self, user_id: str) -> List[Contact]:
        user = self.database["users"].find_one(
            {"_id": ObjectId(user_id)}, {"contacts": 1}
        )
        contacts = user.get("contacts", []) if user else []
        return [Contact(**c) for c in contacts]
