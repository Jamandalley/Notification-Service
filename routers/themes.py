from fastapi import APIRouter, HTTPException
from models.schemas import ThemeModel, ResponseModel, ResponseListModel
import services.theme as service

router = APIRouter()

@router.post("/Create-Theme", response_model=ResponseModel)
def create_theme(theme: ThemeModel):
    service.create_theme(theme)
    return ResponseModel(status="success", message="Theme created successfully")

@router.get("/Get-Themes", response_model=ResponseModel)
def get_theme():
    themes = service.get_theme()
    theme_data_list = []
    if themes:
        for theme in themes:
            theme_data = {
            "name": theme['name'],
            "themeID": str(theme['_id']),
            "templateURL": theme['templateURL'],
            "manifest": theme['manifest'],
            "placeHolderSymbol": theme['placeHolderSymbol'],
            "placeHolder": theme['placeHolder']
        }
            theme_data_list.append(theme_data)
        return ResponseModel(status="success", message="Theme retrieved successfully", data=theme_data_list)
    elif themes == []:
        return ResponseModel(status="success", message="Theme retrieved successfully", data=[])
    raise HTTPException(status_code=404, detail="Theme not found")

@router.put("/Update-Theme", response_model=ResponseModel)
def update_theme(id: str, theme: ThemeModel):
    result = service.update_theme(id, theme)
    if result:
        return ResponseModel(status="success", message="Theme updated successfully")
    raise HTTPException(status_code=404, detail="Theme not found")

@router.delete("/Delete-Theme", response_model=ResponseModel)
def delete_theme(id: str):
    result = service.delete_theme(id)
    if result.deleted_count:
        return ResponseModel(status="success", message="Theme deleted successfully")
    raise HTTPException(status_code=404, detail="Theme not found")
