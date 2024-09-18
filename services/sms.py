from crud import sms as SMS
from models.schemas import SMSRequest

def send_new_sms(sms: SMSRequest):
    return SMS.send_sms(sms)