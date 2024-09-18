import json
from confluent_kafka import Consumer
from crud.sms import send_sms
from crud.whatsapp import send_whatsappMessage
import asyncio
import json

config_ =  {
        'bootstrap.servers': 'kafka-166681-0.cloudclusters.net:19907',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'SCRAM-SHA-256',
        'sasl.username': 'laut',
        'sasl.password': 'Tolulope890@',
        'group.id': 'Smart.Service',
        'auto.offset.reset': 'earliest',
        'ssl.certificate.location': 'ca.pem',
    }

def create_kafka_consumer():    
    topic = "NotificationPy"
    consumer = Consumer(config_)
    consumer.subscribe([topic])
    return consumer

async def consume_messages(consumer, app_code):
    try:
        while True:
            message = consumer.poll(1.0)
            
            if message is None:
                print("waiting...")
            elif message.error():
                print(f"ERROR: {message.error()}")
            else: 
                val = message.value().decode('utf-8')
                print(val)
                data = json.loads(val)
                        
                sms_sent = await send_sms(data["country_code"], data['mobile_number'], data["message"], app_code)
                if sms_sent:
                    print("SMS sent successfully")
                    return True
                else:
                    print("Failed to send SMS to provider")
                    return False
            
    except KeyboardInterrupt:
        print("Consumption interrupted by user")
    finally:
        consumer.close()

async def consume_whatsapp_messages(consumer, app_code):
    try:
        while True:
            message = consumer.poll(1.0)
            
            if message is None:
                print("waiting...")
            elif message.error():
                print(f"ERROR: {message.error()}")
            else: 
                val = message.value().decode('utf-8')
                print(val)
                data = json.loads(val)
                        
                sms_sent = await send_whatsappMessage(data["country_code"], data['mobile_number'], data["message"], app_code)
                if sms_sent:
                    print("SMS sent successfully")
                    return True
                else:
                    print("Failed to send SMS to provider")
                    return False
            
    except KeyboardInterrupt:
        print("Consumption interrupted by user")
    finally:
        consumer.close()
