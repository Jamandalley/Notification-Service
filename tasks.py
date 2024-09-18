# notifications/tasks.py

def send_sms(client, sender, to, message):
    client.messages.create(
        body=message,
        from_=sender,
        to=to
    )

def send_whatsapp(client, sender, to, message):
    client.messages.create(
        body=message,
        from_='whatsapp:' + sender,
        to='whatsapp:' + to
    )
