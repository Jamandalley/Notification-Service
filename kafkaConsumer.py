from confluent_kafka import Consumer
from dotenv import load_dotenv
import os

load_dotenv
config_ = os.getenv("KAFKA_CONSUMER_CONFIG")

def create_kafka_consumer():    
    topic = "NotificationPy"
    consumer = Consumer(config_)
    consumer.subscribe([topic])
    return consumer
