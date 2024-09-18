from pymongo import MongoClient
from models.schemas import ProviderUserModel
from database import get_database
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from bson.objectid import ObjectId

db = get_database()

def create_provider_user(provider_user: ProviderUserModel):
    db.provider_users.insert_one(provider_user)
    return True

def get_all_users():
    try:
        provider_users = db.provider_users.find()
        return list(provider_users)
    except ServerSelectionTimeoutError:
        return []
    except ConnectionFailure:
        return []
    except Exception as e:
        return []

def get_provider_user(user_id: str):
    try:
        object_id = ObjectId(user_id)
    except:
        return None  
    provider = db.provider_users.find_one({"_id": object_id})
    return provider

def update_provider_user(id: str, provider_user: ProviderUserModel):
    object_id = ObjectId(id)
    provider_user_dict = dict(provider_user)
    initial_data = db.provider_users.find_one({"_id": object_id})
    if provider_user_dict['SecretReference'] == initial_data['SecretReference']:
        db.provider_users.update_one({"_id": object_id}, {"$set": provider_user_dict})
        return True
    return False

def delete_provider_user(id: str):
    object_id = ObjectId(id)
    result = db.provider_users.delete_one({"_id": object_id})
    return True
