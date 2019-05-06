# Copyright (c) 2018-2019 Mx (Shift Project delegate / 4446910057799968777S)
# Licensed under MIT License <see LICENSE file>

import requests
import base64
import json


def Telegram(keys, message, parse_mode='HTML', disable_notification=True):
    """
    Sends a message to Telegram and returns response.

    Markdown mode is disabled, cuz it got error with Ryver's markdown and
    delegates usernames with '_' symbol.
    HTML mode enabled.
    """

    # &parse_mode=Markdown
    url = (
        'https://api.telegram.org/bot{apiKey}/sendMessage?chat_id={chat_id}'
        '&parse_mode={parse_mode}&disable_notification={disable_notification}'
        '&text={msg}'.format(
            msg=message, parse_mode=parse_mode,
            disable_notification=disable_notification, **keys
        )
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

    payload['extras'] = {
        "from": {
            "__descriptor": "TestNet Bot"
        }
    }

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


def Discord(keys, message, delete=False):
    """
    Sends a message to Discord and returns response.
    Response contains an 'id' of the sent message.
    """

    url = (
        'https://discordapp.com/api/channels/{channelID}/messages'
        ).format(**keys)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': ''
    }

    headers['Authorization'] = 'Bot {authKey}'.format(**keys)

    if not delete:
        payload = {
            "content": message
        }

        response = requests.post(
            url, data=json.dumps(payload), headers=headers
            )

        return response

    else:
        url_del = url + '/{id}'.format(id=message)
        response = requests.delete(url_del, headers=headers)

        return response


def Discord_channel_data(keys, message):
    """
    Changes a title of a Discord audio channel.
    """

    url = ('https://discordapp.com/api/'
                    'channels/{audioChannelId}').format(**keys)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': ''
    }

    headers['Authorization'] = 'Bot {authKey}'.format(**keys)

    payload = {
        "name": '{message}'.format(message=message)
    }

    response = requests.patch(
        url, data=json.dumps(payload), headers=headers
        )

    return response


# Depreciated
def Discord_webhook(keys, message):
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
