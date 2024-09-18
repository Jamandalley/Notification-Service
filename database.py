from urllib.parse import quote_plus

from pymongo import MongoClient

def get_database():
    username = "admin"
    password = "Tolulope890@"
    ip_address = "204.12.227.216"
    port = 27017  # Specify your port here

    # URL-encode the username and password
    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)

    # Connection string with encoded credentials and port
    connection_string = f"mongodb://{encoded_username}:{encoded_password}@{ip_address}:{port}/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(connection_string)

    return client.notification_system
