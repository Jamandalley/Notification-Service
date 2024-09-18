from fastapi import FastAPI
from routers import providers, provideradmin, themes, appsetup, sms, whatsapp, provideruser

app = FastAPI()

app.include_router(providers.router, prefix="/providers", tags=["providers"])
app.include_router(provideradmin.router, prefix="/provideradmin", tags=["provider_administrators"])
app.include_router(provideruser.router, prefix="/provideruser", tags=["provider_user"])
app.include_router(themes.router, prefix="/themes", tags=["themes"])
app.include_router(appsetup.router, prefix="/applications", tags=["app_setups"])
app.include_router(sms.router, prefix="/sms", tags=["SMS_services"])
app.include_router(whatsapp.router, prefix="/whatsApp", tags=["WhatsApp_Messaging"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Notification System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    