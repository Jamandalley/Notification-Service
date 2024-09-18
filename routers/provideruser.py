from fastapi import APIRouter, HTTPException
from models.schemas import ProviderUserModel, ResponseModel, ResponseListModel
import services.provider_user as service

router = APIRouter()

@router.post("/Create-User", response_model=ResponseModel)
def create_provider_user(provider_user: ProviderUserModel):
    provider_user_dict = dict(provider_user)
    for k, v in provider_user_dict.items():
        if v is not None:
            service.create_provider_user(provider_user_dict)
            return ResponseModel(status="success", message="User created successfully")
        raise HTTPException(status_code=404, detail="Server Error")
    
@router.get("/Get-Users", response_model=ResponseListModel)
def get_provider_user():
    users = service.get_all_users()
    users_list = []
    
    for user in users:
        user_data = {
            "Name": user['ClientReference'],
            "UserID": str(user['_id']),
            "Password": "*****"
        }
        users_list.append(user_data)
    
    if users_list:
        return ResponseListModel(status="success", message="Request was successful", data=users_list)
    elif users_list == []:
        return ResponseListModel(status="success", message="Request was successful")
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch users")

@router.get("/Get-User", response_model=ResponseModel)
def get_provider_user(user_id: str):
    user = service.get_provider_user(user_id)
    if user:
        user_data = {
            "Name": user['ClientReference'],
            "UserID": str(user['_id']),
            "Password": "*****"
        }
        return ResponseModel(status="success", message="Provider retrieved successfully", data=user_data)
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/Update-User", response_model=ResponseModel)
def update_provider_user(id: str, provider_user: ProviderUserModel):
    result = service.update_provider_user(id, provider_user)
    if result:
        return ResponseModel(status="success", message="User updated successfully")
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/Delete-User", response_model=ResponseModel)
def delete_user(id: str):
    result = service.delete_provider_user(id)
    if result:
        return ResponseModel(status="success", message="User deleted successfully")
    raise HTTPException(status_code=404, detail="User not found")
