# scoop bucket add twilio-scoop https://github.com/twilio/scoop-twilio-cli
# twilio
import os
from twilio.rest import Client

# twilio send message
# Download the helper library from https://www.twilio.com/docs/python/install

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = 'AC3f4671ad205449a5b0a09139dd785632'
auth_token = 'c9de7cc354691cbd0a768d82915ce5bd'
client = Client(account_sid, auth_token)
base_twilio_number = '+13167666830'


def send_message(number, text_message):
    message = client.messages \
                .create(
                     body=text_message,
                     from_=base_twilio_number,
                     to=number
                 )

    print(message.sid)

#send_message('+19717169732', 'hello testing message')