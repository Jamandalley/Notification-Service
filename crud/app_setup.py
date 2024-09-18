import uuid
from pymongo import MongoClient
from models.schemas import AppSetupModel
from database import get_database
from bson.objectid import ObjectId

db = get_database()

def create_app_setup(app_setup: AppSetupModel):
    app_setup_dict = app_setup.dict()
    app_theme = db.sms_themes.find_one({"_id": ObjectId(app_setup_dict['themeId'])})
    user_details = db.provider_users.find_one({"_id": ObjectId(app_setup_dict['ProviderUserId'])})
    provider_id = str(user_details['ProviderId'])
    app_config = db.providers.find_one({"_id": ObjectId(provider_id)})
    app_config_dict = {}
    app_config_dict = {
        "UserID": app_setup_dict['ProviderUserId'],
        "AppName": app_setup_dict['AppName'],
        "Theme": app_theme['manifest'],
        "AppSID": app_config['ProviderSID'],
        "AppAuthToken": app_config['ProviderAuthToken'],
        "ServiceSID": app_config['ServiceSID']
    }
    # app_setup_dict["AppCode"] = str(uuid.uuid4()).replace("-", "")
    db.app_setups.insert_one(app_config_dict)
    return True

def get_app_setup():
    result = db.app_setups.find()
    return list(result)

def delete_app_setup(user_id: str):
    db.app_setups.delete_one({"UserID": user_id})
    return True
