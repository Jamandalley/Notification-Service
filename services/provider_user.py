from crud import provider_user as crud
from models.schemas import ProviderUserModel, ProviderType
from typing import Any, Dict

def create_provider_user(provider_user: ProviderUserModel):
    return crud.create_provider_user(provider_user)

def get_all_users():
    return crud.get_all_users()

def get_provider_user(id: str):
    return crud.get_provider_user(id)

def update_provider_user(id: str, provider_user: ProviderUserModel):
    return crud.update_provider_user(id, provider_user)

def delete_provider_user(id: str):
    return crud.delete_provider_user(id)

def convert_document(document: Dict) -> Dict:
    if document and "_id" in document:
        document["_id"] = str(document["_id"])
    if "Type" in document:
        document["Type"] = ProviderType(document["Type"]).name
    return document