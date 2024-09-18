from pymongo import MongoClient, ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from models.schemas import ProviderModel
from database import get_database
from bson.objectid import ObjectId

db = get_database()

def create_provider(provider: ProviderModel):
    provider_dict = dict(provider)
    result = db.providers.insert_one(provider_dict)
    return True

def get_all_providers():
    try:
        providers = db.providers.find()
        return list(providers)
    except ServerSelectionTimeoutError:
        return []
    except ConnectionFailure:
        return []
    except Exception as e:
        return []

def get_provider(provider_id: str):
    try:
        object_id = ObjectId(provider_id)
    except:
        return None  
    provider = db.providers.find_one({"_id": object_id})
    return provider

def update_provider(provider_id: str, admin_id: str, provider: ProviderModel):
    object_id = ObjectId(provider_id)
    provider = dict(provider)
    provider["Type"] = provider["Type"].value
    updated_document = db.providers.find_one_and_update(
        {"_id": object_id, "adminID": admin_id},
        {"$set": provider},
        return_document=ReturnDocument.AFTER
    )
    return True

def delete_provider(provider_id: str, admin_id: str):
    db = get_database()
    object_id = ObjectId(provider_id)
    result = db.providers.delete_one({"_id": object_id, "adminID": admin_id})
    return True