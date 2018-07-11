# -*- coding: utf-8 -*-
import requests
import base64
import json


def Telegram(message, keys):
    url = (
        'https://api.telegram.org/bot{apiKey}/sendMessage?chat_id={chat_id}'
        '&parse_mode=Markdown&text={msg}'.format(msg=message, **keys)
    )
    response = requests.get(url)
    return response


def Ryver(message, keys):
    url = (
        'https://{projectName}.ryver.com/api/1/odata.svc/forums({forumID})'
        '/Chat.PostMessage()'.format(**keys)
    )
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': ''
    }
    auth = str(
        base64.b64encode('{login}:{password}'.format(**keys).encode('utf-8'))
        .decode('utf-8')
    )
    headers['Authorization'] = 'Basic ' + auth

    payload = {}
    payload["body"] = message

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.text
