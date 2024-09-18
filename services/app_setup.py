from crud import app_setup as crud
from models.schemas import AppSetupModel

def create_app_setup(app_setup: AppSetupModel):
    return crud.create_app_setup(app_setup)

def get_app_setup():
    return crud.get_app_setup()

def delete_app_setup(user_id: str):
    return crud.delete_app_setup(user_id)
