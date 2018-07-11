# Copyright (c) 2018 Mx (Shift Project delegate / 4446910057799968777S)
# Licensed under MIT License <see LICENSE file>

import requests
import base64
import json


def Telegram(keys, message):
    """
    Sends a message to Telegram and returns response.

    Markdown mode is disabled, cuz it got error with Ryver's markdown and
    delegates usernames with '_' symbol.
    HTML mode enabled.
    """

    # &parse_mode=Markdown
    url = (
        'https://api.telegram.org/bot{apiKey}/sendMessage?chat_id={chat_id}'
        '&parse_mode=HTML&text={msg}'.format(msg=message, **keys)
    )
    response = requests.get(url)
    return response


def Ryver(keys, message, delete=False):
    """
    Sends a message to Ryver and returns response.
    Response contains an 'id' of sent message.
    """

    payload = {}

    if not delete:
        action = 'Post'
        payload['body'] = message
    else:
        action = 'Delete'
        payload['id'] = message

    url = (
        'https://{projectName}.ryver.com/api/1/odata.svc/forums({forumID})'
        '/Chat.{action}Message()'.format(action=action, **keys)
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

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response


def Discord(keys, message):
    """
    Post a message to discord API via a Webhook.
    """

    url = keys['webhook_url']

    payload = {
        "content": message
    }

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response
