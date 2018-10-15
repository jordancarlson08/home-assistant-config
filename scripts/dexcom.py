import requests
import json
import logging


homeAssistantToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4NTQ5OTQ1OTQsImlzcyI6IjliYzcyZGU1MzNkNTQ2NWRiNThmNDQ0MzQ1M2RhNGExIiwiaWF0IjoxNTM5NjM0NTk0fQ.xg5s5xEfRJdf8X2ReuAdtqPJZm8TnSUymTTQMJ3eeYk'

accountId = '5cc8c7af-b374-47da-a539-39e2723c606c'
applicationId = 'D89443D2-327C-4A6F-89E5-496BBB0317DB'
password = '100b5265dc7a44a7b0ab9be9c3ff9d8f'

baseUrl = 'https://share2.dexcom.com/ShareWebServices/Services/'
getSessionId = 'General/LoginSubscriberAccount'
getSubscriptions = 'Subscriber/ListSubscriberAccountSubscriptions'
getReadings = 'Subscriber/ReadSubscriptionLatestGlucoseValues'

data = json.dumps({
    'accountId': accountId,
    'applicationId': applicationId,
    'password': password
})

headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; SM-G955U Build/NRD90M)'
}

# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1
#
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

response = requests.post(baseUrl + getSessionId, headers=headers, data=data)

# print(response.text)

if response.status_code == 200:
    sessionToken = response.text
    token = sessionToken.replace('"', '')
    urlParams = {'sessionId': token}

    subHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; SM-G955U Build/NRD90M)',
        'Accept-Enncoding': 'gzip'
    }

    subscriberResponse = requests.post(baseUrl + getSubscriptions, params=urlParams, headers=subHeaders)

    # print(subscriberResponse.text)
    jsonResp = json.loads(subscriberResponse.text)
    subId = jsonResp[0].get('SubscriptionId')

    if subscriberResponse.status_code == 200:
        params = {'sessionId': token,
                  'subscriptionId': subId,
                  'minutes': 5,
                  'maxCount': 1}

        reading = requests.post(baseUrl + getReadings, params=params, headers=subHeaders)

        latestValue = json.loads(reading.text)[0].get('Value')

        print(latestValue)
