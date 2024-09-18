from pymongo import MongoClient
from models.schemas import ThemeModel
from database import get_database
from bson.objectid import ObjectId

db = get_database()

def create_theme(theme: ThemeModel):
    theme_dict = theme.dict()
    db.sms_themes.insert_one(theme_dict)
    return True

def get_theme():
    result = db.sms_themes.find()
    return list(result)

def update_theme(id: str, theme: ThemeModel):
    theme_dict = dict(theme)
    object_id = ObjectId(id)
    db.sms_themes.update_one({"_id": object_id}, {"$set": theme_dict})
    return True

def delete_theme(id: str):
    object_id = ObjectId(id)
    return db.sms_themes.delete_one({"_id": object_id})
