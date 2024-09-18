from confluent_kafka import Producer
from models.schemas import SMSRequest
import json

config_ =  {
    'bootstrap.servers': 'kafka-166681-0.cloudclusters.net:19907',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'SCRAM-SHA-256',
    'sasl.username': 'laut',
    'sasl.password': 'Tolulope890@',
    # 'group.id': 'Smart.Service',
    # 'auto.offset.reset': 'earliest',
    'ssl.certificate.location': 'ca.pem',
    }

def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print(msg.value().decode('utf-8'))

def produce_message(country_code, mobile_number, message):
    topic = "NotificationPy"
    producer = Producer(config_)

    sms_data = {
        "country_code": country_code,
        "mobile_number": mobile_number,
        "message": message
    }
    
    sms_data_json = json.dumps(sms_data)
    
    producer.produce(topic, sms_data_json.encode('utf-8'), callback=delivery_callback) 
    
    producer.poll(10000)
    producer.flush()