import requests, json

def sendNotification(message, token):
    headers = {
        'Content-Type': 'application/json',
    }

    data = json.dumps({"value1": message})

    response = requests.post(
        f'https://maker.ifttt.com/trigger/notification/with/key/{token}',
        headers=headers, data=data)
    return response.status_code
