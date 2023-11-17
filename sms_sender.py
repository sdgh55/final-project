from twilio.rest import Client
import os


account_sid = ('AC7ead19981e77d3ab3167d582cab92016')
auth_token = ('93769501913d29deed694ba9eff01336')
client = Client(account_sid, auth_token)


message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+77775092639',
                     to='+77028331578'
                 )

print(message.sid)