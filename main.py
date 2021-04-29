import os
import math
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# the API without the key:value needed at the end. Those go into parameters
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'YourSid'
auth_token = 'Auth_Token'

parameters = {
    "lat": 40.678177,
    "lon": -73.944160,
    "exclude": "hourly,alerts,current,minutely",
    # stored in environment variable. To view type env in terminal
    "appid": "App_ID"
}

response = requests.get(OWM_Endpoint, params=parameters)

# used for debugging the requests module and is an integral part of Python requests
response.raise_for_status()
data = response.json()

# daily high and low temps
daily_low_temp = int(data["daily"][0]["temp"]["min"])
daily_high_temp = int(data["daily"][0]["temp"]["max"])

# convert to fahrenheit
fahrenheit_low = math.floor((daily_low_temp - 273.15) * (9 / 5) + 32)
fahrenheit_high = math.floor((daily_high_temp - 273.15) * (9 / 5) + 32)

# is it raining, sunny, snowing?
weather = data["daily"][0]["weather"][0]["description"]



# to get twilio to work on free account with the proxy
proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}
client = Client(account_sid, auth_token, http_client=proxy_client)





message = client.messages \
    .create(
    body=f"It will be between {fahrenheit_low} and {fahrenheit_high} today with {weather}.",
    from_='+14704104494',
    to='+16466100081')



print(message.status)
