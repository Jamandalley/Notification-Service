from fastapi import APIRouter, HTTPException
from models.schemas import ProviderModel, ResponseModel, ResponseListModel
import services.provider as service
 
router = APIRouter()

@router.post("/", response_model=ResponseModel)
def create_provider(provider: ProviderModel):
    provider_data = dict(provider)
    provider_data["Type"] = provider_data["Type"].value
    if provider_data['Type'].upper() == "SMS" or "WHATSAPP" and len(provider_data['ProviderSID'])==34:
        created_provider = service.create_new_provider(provider_data)
        if created_provider:
            return ResponseModel(status="success", message="Provider created successfully")
        else:
            raise HTTPException(status_code=500, status= "failed", detail="Failed to create provider")
    else:
        raise HTTPException(status_code=500, detail="Provider type not supported")
    
@router.get("/Get-Providers", response_model=ResponseListModel)
def get_all_providers():
    providers = service.get_all_providers()
    provider_data_list = []
    
    for provider in providers:
        provider_data = {
            "Name": provider['Type'],
            "ProviderSID": provider['ProviderSID'],
            "ProviderAuthToken": provider['ProviderAuthToken'],
            "ServiceSID": provider['ServiceSID'],
            "ProviderID": str(provider['_id'])
        }
        provider_data_list.append(provider_data)
    
    if provider_data_list:
        return ResponseListModel(status="success", message="Request was successful", data=provider_data_list)
    elif provider_data_list == []:
        return ResponseListModel(status="success", message="Request was successful", data=[])
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch providers")

@router.get("/Get-Provider", response_model=ResponseModel)
def get_provider(provider_id: str):
    provider = service.get_existing_provider(provider_id)
    if provider:
        provider_data = {
            "Name": provider['Type'],
            "ProviderSID": provider['ProviderSID'],
            "ProviderAuthToken": provider['ProviderAuthToken'],
            "ServiceSID": provider['ServiceSID'],
            "ProviderID": str(provider['_id'])
        }
        return ResponseModel(status="success", message="Provider retrieved successfully", data=provider_data)
    raise HTTPException(status_code=404, detail="Provider not found")

@router.put("/Update-Provider", response_model=ResponseModel)
def update_provider(provider_id: str, admin_id: str, provider: ProviderModel):
    updated_provider = service.update_existing_provider(provider_id, admin_id, provider)
    if updated_provider:
        return ResponseModel(status="success", message="Provider updated successfully")
    raise HTTPException(status_code=404, detail="Provider not found")

@router.delete("/{provider_id}", response_model=ResponseModel)
def delete_provider(provider_id: str, admin_id):
    result = service.delete_existing_provider(provider_id, admin_id)
    if result:
        return ResponseModel(status="success", message="Provider deleted successfully")
    raise HTTPException(status_code=404, detail="Provider not found")
