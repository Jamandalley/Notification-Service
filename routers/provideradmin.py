from fastapi import APIRouter, HTTPException
from models.schemas import ProviderAdministratorModel, ResponseModel, ResponseListModel
import services.provider_administrator as service

router = APIRouter()

@router.post("/Create-Admin", response_model=ResponseModel)
def create_provider_administrator(provider_administrator: ProviderAdministratorModel):
    provider_administrator_dict = dict(provider_administrator)
    for k, v in provider_administrator_dict.items():
        if v is not None:
            service.create_provider_administrator(provider_administrator_dict)
            return ResponseModel(status="success", message="You have scuccessfully registered as an Admin")
        raise HTTPException(status_code=404, detail="Server Error")
    

@router.get("/Get-Admins", response_model=ResponseModel)
def get_provider_administrator():
    admins = service.get_all_admins()
    admins_list = []
    
    for admin in admins:
        admin_data = {
            "Name": admin['ClientReference'],
            "AdminID": str(admin['_id']),
            "Password": "*****"
        }
        admins_list.append(admin_data)
    
    if admins_list:
        return ResponseListModel(status="success", message="Request was successful", data=admins_list)
    elif admins_list == []:
        return ResponseListModel(status="success", message="Request was successful", data=[])
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch admins")

@router.get("/Get-Admin", response_model=ResponseModel)
def get_provider_administrator(admin_id: str):
    admin = service.get_provider_administrator(admin_id)
    if admin:
        admin_data = {
            "Name": admin['ClientReference'],
            "AdminID": str(admin['_id']),
            "Password": "*****"
        }
        return ResponseModel(status="success", message="Request was successful", data=admin_data)
    raise HTTPException(status_code=404, detail="Provider not found")

# @router.put("/{id}", response_model=ResponseModel)
# def update_provider_administrator(id: str, provider_administrator: ProviderAdministratorModel):
#     result = service.update_provider_administrator(id, provider_administrator)
#     if result:
#         return ResponseModel(status="success", message="Provider Administrator updated successfully")
#     raise HTTPException(status_code=404, detail="Provider Administrator not found")

@router.delete("/Delete-Admin", response_model=ResponseModel)
def delete_provider_administrator(id: str):
    result = service.delete_provider_administrator(id)
    if result:
        return ResponseModel(status="success", message="Provider Administrator deleted successfully")
    raise HTTPException(status_code=404, detail="Provider Administrator not found")
