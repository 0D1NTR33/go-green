# -*- coding: utf-8 -*-
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
    Post a message to discord api via a bot.
    Bot must be added to the server and have write access to the channel.
    You may need to connect with a websocket the first time you run the bot
    You can use a library like discord.py to do so.
    """

    # enable dev mode on discord, right-click on the channel, copy ID
    channelID = keys['Channel ID']
    # get from the bot page. must be a bot, not a discord app
    botToken = keys['Bot token']

    baseURL = (
        'https://discordapp.com/api/channels/{}/messages'
        .format(channelID)
    )
    headers = {
        'Authorization': 'Bot {}'.format(botToken),
        'User-Agent': 'myBotThing (http://some.url, v0.1)',
        'Content-Type': 'application/json'
    }

    POSTedJSON = json.dumps({'content': message})

    response = requests.post(baseURL, headers=headers, data=POSTedJSON)
    return response
