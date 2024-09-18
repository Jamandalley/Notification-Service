from twilio.rest import Client
from models.schemas import SMSRequest
from database import get_database
from bson.objectid import ObjectId
import asyncio

db = get_database()

async def send_sms(country_code, mobile_number, message, appcode):
    try:
        app_config = db.app_setups.find_one({"_id": ObjectId(appcode)})
        TWILIO_SID= app_config['AppSID']
        TWILIO_AUTH_TOKEN = app_config['AppAuthToken']
        TWILIO_SERVICE_SID = app_config['ServiceSID']
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        countryCode = country_code
        mobileNumber = mobile_number
        message = message
        if isinstance(mobileNumber, list):
            results = []
            for number in mobileNumber:
                recipient = countryCode + number
                try:
                    msg = client.messages.create(
                        body=message,
                        from_=TWILIO_SERVICE_SID,
                        to=recipient
                    )
                    results.append(msg.sid is not None)
                except Exception as e:
                    results.append(False)
            return all(results)
        else:
            recipient = countryCode + mobileNumber
            try:
                msg = client.messages.create(
                    body=message,
                    from_=TWILIO_SERVICE_SID,
                    to=recipient
                )
                return msg.sid is not None
            except Exception as e:
                return False
    except Exception as e:
        print(f"Exception in send_sms_to_provider: {e}")
        return False