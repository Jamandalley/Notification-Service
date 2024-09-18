from crud import whatsapp as WhatsApp
from models.schemas import WhatsAppRequest

def send_new_whatsappMsg(whatsAp: WhatsAppRequest):
    return WhatsApp.send_whatsappMessage(whatsAp)