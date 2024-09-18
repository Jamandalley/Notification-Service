from pymongo import MongoClient
from models.schemas import ProviderAdministratorModel, ProviderUserModel
from database import get_database
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from bson.objectid import ObjectId

db = get_database()

def create_provider_administrator(provider_administrator: ProviderAdministratorModel):
    db.provider_administrators.insert_one(provider_administrator)
    return True

def get_all_admins():
    try:
        provider_admins = db.provider_administrators.find()
        return list(provider_admins)
    except ServerSelectionTimeoutError:
        return []
    except ConnectionFailure:
        return []
    except Exception as e:
        return []

def get_provider_administrator(admin_id: str):
    try:
        object_id = ObjectId(admin_id)
    except:
        return None  
    provider = db.provider_administrators.find_one({"_id": object_id})
    return provider

def update_provider_administrator(id: str, provider_administrator: ProviderAdministratorModel):
    provider_administrator_dict = dict(provider_administrator)
    result = db.provider_administrators.update_one({"Id": id}, {"$set": provider_administrator_dict})
    return True

def delete_provider_administrator(id: str):
    object_id = ObjectId(id)
    result = db.provider_administrators.delete_one({"Id": object_id})
    return True
