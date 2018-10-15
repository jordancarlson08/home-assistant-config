import requests
import json

ACCOUNT_ID = '5cc8c7af-b374-47da-a539-39e2723c606c'
APPLICATION_ID = 'D89443D2-327C-4A6F-89E5-496BBB0317DB'
PASSWORD = '100b5265dc7a44a7b0ab9be9c3ff9d8f'

BASE_URL = 'https://share2.dexcom.com/ShareWebServices/Services/'
SESSION_ID_URL = 'General/LoginSubscriberAccount'
SUBSCRIPTIONS_URL = 'Subscriber/ListSubscriberAccountSubscriptions'
READINGS_URL = 'Subscriber/ReadSubscriptionLatestGlucoseValues'


def get_session_token():
    global sessionResponse
    sessionData = json.dumps({
        'accountId': ACCOUNT_ID,
        'applicationId': APPLICATION_ID,
        'password': PASSWORD
    })
    sessionHeaders = {
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; SM-G955U Build/NRD90M)'
    }
    sessionResponse = requests.post(BASE_URL + SESSION_ID_URL, headers=sessionHeaders, data=sessionData)

    if sessionResponse.status_code == 200:
        get_subscription_id()


def get_subscription_id():
    global token, subHeaders, subscriberResponse, subId
    sessionToken = sessionResponse.text
    token = sessionToken.replace('"', '')
    subParams = {'sessionId': token}
    subHeaders = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; SM-G955U Build/NRD90M)',
        'Accept-Enncoding': 'gzip'
    }
    subscriberResponse = requests.post(BASE_URL + SUBSCRIPTIONS_URL, params=subParams, headers=subHeaders)
    subId = json.loads(subscriberResponse.text)[0].get('SubscriptionId')

    if subscriberResponse.status_code == 200:
        get_latest_reading()


def get_latest_reading():
    readingsParams = {'sessionId': token,
                      'subscriptionId': subId,
                      'minutes': 5,
                      'maxCount': 1}
    reading = requests.post(BASE_URL + READINGS_URL, params=readingsParams, headers=subHeaders)
    latestValue = json.loads(reading.text)[0].get('Value')
    print(latestValue)


get_session_token()
