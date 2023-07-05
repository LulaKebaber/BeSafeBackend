from datetime import datetime
from typing import Optional, List

from bson.objectid import ObjectId
from pymongo.database import Database
from ..models import Contact


# fr.om ..router.router_get_contacts import Contact

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
        word_data = {
            "word": word.word,
            "timestamp": word.timestamp,
        }
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={"$push": {"words": word_data}},
        )

    def get_user_words(self, user_id: str):
        user = self.database["users"].find_one({"_id": ObjectId(user_id)}, {"words": 1})
        words = user.get("words", []) if user else []

        # Convert the words list to a list of dictionaries with word and timestamp
        words_with_timestamps = [
            {"word": word["word"], "timestamp": word["timestamp"]} for word in words
        ]

        return words_with_timestamps

    def add_new_contact(self, user_id: str, data: dict):
        contact_data = {
            "name": data["name"],
            "phone": data["phone"],
            "gps": data["gps"],
        }

        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={"$push": {"contacts": contact_data}},
        )

    def get_user_contacts(self, user_id: str) -> List[Contact]:
        user = self.database["users"].find_one(
            {"_id": ObjectId(user_id)}, {"contacts": 1}
        )
        contacts = user.get("contacts", []) if user else []

        # Convert the words list to a list of dictionaries with word and timestamp
        contacts_data = [
            {
                "name": contact["name"],
                "phone": contact["phone"],
                "gps": contact["gps"],
            }
            for contact in contacts
        ]

        return contacts_data
        # user = self.database["users"].find_one({"_id": ObjectId(user_id)})
        # contacts = []
        # for i in range(len(user["phone"])):
        #     contact = Contact(
        #         name=user["name"][i], phone=user["phone"][i], gps=user["gps"][i]
        #     )
        #     contacts.append(contact)
        # return contacts
