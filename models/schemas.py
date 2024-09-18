from pydantic import BaseModel
from typing import Any, Optional, List
from enum import Enum

# Enum for Provider Type
class ProviderType(Enum):
    Email = "Email"
    Sms = "SMS"
    Whatsapp = "WhatsApp"
    PushNotification = "PushNotification"

# Pydantic models for request body validation
class ProviderModel(BaseModel):
    Type: ProviderType
    ProviderSID: str
    ProviderAuthToken: str
    ServiceSID: str
    adminID: str

class ProviderAdministratorModel(BaseModel):
    ClientReference: str
    SecretReference: str
    isenabled: bool

class ProviderUserModel(BaseModel):
    ClientReference: str
    SecretReference: str
    ProviderId: str
    isenabled: bool

# class ThemeModel(BaseModel):
#     themeName: str
#     placeholder: str
#     manifest: str
#     isenabled: bool

class PlaceHolderModel(BaseModel):
    key: str
    value: str

class ThemeModel(BaseModel):
    name: str
    templateURL: Optional[str] = None
    manifest: str
    isenabled: bool
    placeHolderSymbol: str
    placeHolder: List[PlaceHolderModel]

class AppSetupModel(BaseModel):
    AppName: str
    themeId: str
    ProviderUserId: str

# Standardized response model
class ResponseModel(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None

# Standardized response list model
class ResponseListModel(BaseModel):
    status: str
    message: str
    data: Optional[List[Any]] = None

class SMSRequest(BaseModel):
    countryCode: str 
    mobileNumber: str 
    message: str
    AppCode: str

class BulkSMSRequest(BaseModel):
    countryCode: str 
    mobileNumber: List[str]
    message: str
    AppCode: str
    
class WhatsAppRequest(BaseModel):
    countryCode: str 
    mobileNumber: str 
    message: str
    AppCode: str

class BulkWhatsAppRequest(BaseModel):
    countryCode: str 
    mobileNumber: List[str]
    template: Optional[str] = None
    message: str
    AppCode: str