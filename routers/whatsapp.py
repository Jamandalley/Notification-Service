from fastapi import APIRouter, HTTPException
from models.schemas import ResponseModel, WhatsAppRequest, BulkWhatsAppRequest
from services.kafkaProducer import produce_message
from services.kafkaConsumer import create_kafka_consumer, consume_messages, consume_whatsapp_messages
import asyncio
 
router = APIRouter()   
    
@router.post("/message", response_model=ResponseModel)
async def send_whatsApp_message(whatsApp_request: WhatsAppRequest):
    sms_dict = dict(whatsApp_request)
    mobile_number = sms_dict['mobileNumber']
    country_code = sms_dict['countryCode']
    app_code = sms_dict['AppCode']
    message = sms_dict['message']
    
    producer = produce_message(country_code, mobile_number, message)
    
    print(f'This is the app code: {app_code}')
    consumer = create_kafka_consumer()
    message_sent = await consume_whatsapp_messages(consumer, app_code)
        
    if message_sent:
        return ResponseModel(status="success", message="WhatsApp message sent successfully")
    else:
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")

@router.post("/bulk_Message/", response_model=ResponseModel)
async def send_bulk_WhatsApp_message(bulk_whatsapp_request: BulkWhatsAppRequest):
    message_dict = dict(bulk_whatsapp_request)
    mobile_number = message_dict['mobileNumber']
    country_code = message_dict['countryCode']
    app_code = message_dict['AppCode']
    message = message_dict['message']
    
    producer = produce_message(country_code, mobile_number, message)
    
    print(f'This is the app code: {app_code}')
    consumer = create_kafka_consumer()
    message_sent = await consume_whatsapp_messages(consumer, app_code)
    
    results = {}
    for recipient in bulk_whatsapp_request.mobileNumber:
        results[recipient] = "Sent" if message_sent else "Failed"
    
    if message_sent:
        return ResponseModel(status="success", message="WhatsApp Message sent successfully", data=results)
    else:
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp Message")        