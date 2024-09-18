from crud import provider_administrator as crud
from models.schemas import ProviderAdministratorModel, ProviderType
from typing import Any, Dict

def create_provider_administrator(provider_administrator: ProviderAdministratorModel):
    return crud.create_provider_administrator(provider_administrator)

def get_all_admins():
    return crud.get_all_admins()

def get_provider_administrator(id: str):
    return crud.get_provider_administrator(id)

def update_provider_administrator(id: str, provider_administrator: ProviderAdministratorModel):
    return crud.update_provider_administrator(id, provider_administrator)

def delete_provider_administrator(id: str):
    return crud.delete_provider_administrator(id)

def convert_document(document: Dict) -> Dict:
    if document and "_id" in document:
        document["_id"] = str(document["_id"])
    if "Type" in document:
        document["Type"] = ProviderType(document["Type"]).name
    return document