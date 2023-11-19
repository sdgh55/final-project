from twilio.rest import Client

# Initialize Twilio client with your credentials
account_sid = 'AC7ead19981e77d3ab3167d582cab92016'
auth_token = '93769501913d29deed694ba9eff01336'
client = Client(account_sid, auth_token)

# Generate and send verification code
#verification_code = generate_verification_code()  # Implement this function
to_phone_number = '+77775092639'  # Replace with user's phone number
from_phone_number = '+77775092639'  # Replace with your Twilio phone number

message = client.messages.create(
    body=f'Your verification code is:',
    from_=from_phone_number,
    to=to_phone_number)
