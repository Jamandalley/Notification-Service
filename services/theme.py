from crud import theme as crud
from models.schemas import ThemeModel
from typing import Dict

def create_theme(theme: ThemeModel):
    return crud.create_theme(theme)

def get_theme():
    return crud.get_theme()

def update_theme(id: str, theme: ThemeModel):
    return crud.update_theme(id, theme)

def delete_theme(id: str):
    return crud.delete_theme(id)

def convert_document(document: Dict) -> Dict:
    if document and "_id" in document:
        document["themeID"] = str(document["_id"])
    return document
