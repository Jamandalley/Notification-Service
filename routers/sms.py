from fastapi import APIRouter, HTTPException
from models.schemas import ResponseModel, SMSRequest, BulkSMSRequest
import services.sms as sms
from services.kafkaProducer import produce_message
from services.kafkaConsumer import create_kafka_consumer, consume_messages
import asyncio

router = APIRouter()   

@router.post("/", response_model=ResponseModel)
async def send_sms(sms_request: SMSRequest):
    sms_dict = dict(sms_request)
    mobile_number = sms_dict['mobileNumber']
    country_code = sms_dict['countryCode']
    app_code = sms_dict['AppCode']
    message = sms_dict['message']
    
    producer = produce_message(country_code, mobile_number, message)
    
    print(f'This is the app code: {app_code}')
    consumer = create_kafka_consumer()
    sms_sent = await consume_messages(consumer, app_code)
        
    if sms_sent:
        return ResponseModel(status="success", message="SMS sent successfully")
    else:
        raise HTTPException(status_code=500, detail="Failed to send SMS")
    # raise HTTPException(status_code=500, detail="Failed to send SMS")

@router.post("/bulk_sms/", response_model=ResponseModel)
async def send_bulk_sms(bulk_sms_request: BulkSMSRequest):
    sms_dict = dict(bulk_sms_request)
    mobile_number = sms_dict['mobileNumber']
    country_code = sms_dict['countryCode']
    app_code = sms_dict['AppCode']
    message = sms_dict['message']
    
    producer = produce_message(country_code, mobile_number, message)
    
    print(f'This is the app code: {app_code}')
    consumer = create_kafka_consumer()
    sms_sent = await consume_messages(consumer, app_code)
    
    results = {}
    for recipient in bulk_sms_request.mobileNumber:
        results[recipient] = "Sent" if sms_sent else "Failed"
    
    if sms_sent:
        return ResponseModel(status="success", message="SMS sent successfully", data=results)
    else:
        raise HTTPException(status_code=500, detail="Failed to send SMS")        