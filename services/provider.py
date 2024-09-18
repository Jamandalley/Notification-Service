from crud import provider as crud
from models.schemas import ProviderModel, ProviderType
from typing import Any, Dict

def create_new_provider(provider: ProviderModel):
    return crud.create_provider(provider)

def get_all_providers():
    return crud.get_all_providers()

def get_existing_provider(provider_id: str):
    return crud.get_provider(provider_id)

def update_existing_provider(provider_id: str, admin_id: str, provider: ProviderModel):
    return crud.update_provider(provider_id, admin_id, provider)

def delete_existing_provider(provider_id: str, admin_id: str):
    return crud.delete_provider(provider_id, admin_id)

def convert_document(document: Dict) -> Dict:
    if document and "_id" in document:
        document["_id"] = str(document["_id"])
    # if "Type" in document:
    #     document["Type"] = ProviderType(document["Type"]).name
    return document