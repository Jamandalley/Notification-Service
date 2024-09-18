from fastapi import APIRouter, HTTPException
from models.schemas import AppSetupModel, ResponseModel, ResponseListModel
import services.app_setup as service

router = APIRouter()

@router.post("/Cofigure-Application", response_model=ResponseModel)
def create_app_setup(app_setup: AppSetupModel):
    created_app_setup = service.create_app_setup(app_setup)
    return ResponseModel(status="success", message="App configured successfully")

@router.get("/Get-Applications", response_model=ResponseModel)
def get_app_setup():
    apps = service.get_app_setup()
    app_list = []
    
    for app in apps:
        app_data = {
            "AppName": app['AppName'],
            "AppCode": str(app['_id'])
        }
        app_list.append(app_data)
    
    if app_list:
        return ResponseListModel(status="success", message="Request was successful", data=app_list)
    elif app_list==[]:
        return ResponseListModel(status="success", message="Request was successful", data=[])
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch providers")
    
@router.delete("/Delete-Application", response_model=ResponseModel)
def delete_app_setup(providerUserID: str):
    result = service.delete_app_setup(providerUserID)
    if result:
        return ResponseModel(status="success", message="App setup deleted successfully")
    raise HTTPException(status_code=404, detail="App setup not found")
