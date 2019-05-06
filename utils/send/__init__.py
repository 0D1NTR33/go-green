# Copyright (c) 2018-2019 Mx (Shift Project delegate / 4446910057799968777S)
# Licensed under MIT License <see LICENSE file>

import json

from . import messengers
from data import config

telegram_config = config.telegram
telegram_debug = config.telegram_debug
ryver_config = config.ryver

if config.discord:
    discord_config = config.discord
else:
    discord_config = config.discord_wh

delete = True

markdown_syntax = {
    'bold': '**',
    'bold_close': '**',
    'italic': '_',
    'italic_close': '_',
    'out': ':heavy_minus_sign:',
    'in': ':heavy_plus_sign:',
    'check_mark': ':white_check_mark:'
}

html_syntax = {
    'bold': '<b>',
    'bold_close': '</b>',
    'italic': '<i>',
    'italic_close': '</i>',
    'out': '%E2%9E%96',
    'in': '%E2%9E%95',
    'check_mark': '%E2%9C%85',
    'd1': '',
    'd2': '',
    'separator': ''
}

discord_syntax = {
    'bold': '**',
    'bold_close': '**',
    'italic': '*',
    'italic_close': '*',
    'out': ':outbox_tray:',
    'in': ':inbox_tray:',
    'check_mark': ':white_check_mark:',
    'd1': '<',
    'd2': '>',
    'separator': ':wavy_dash:'
}

good_msg = (
    '{bold}{name}{bold_close} is now green! {check_mark} \n'
    'Not forging time: {bold}{time}{bold_close} {smile}\n'
    '{separator}'
)

missed_block_string = '{italic}Missed block{italic_close}\n'

bad_msg = (
    'Delegate: {bold}{Name}{bold_close} / {d1}@{Username}{d2}\n'
    'Last block forged: {bold}{lastBlockTime}{bold_close}\n'
    '{bold}Next turn:{bold_close} {NextTurn}\n'
    '{separator}'
)

message_explorers = (
    '{bold}Bot is not working{bold_close}\n'
    'Explorer: {url} \n'
    'Online: {bold}{status}{bold_close}\n\n'
    'Mirror: {url_mirror} \n'
    'Online: {bold}{status_mirror}{bold_close}\n\n'
)


def ChooseClockSmile(time):
    clock = ':clock{num}:'

    time = time.split(' ')

    if 'hour' in time:
        return ':zap:'

    if 'hours' in time and int(time[0]) <= 12:
        return clock.format(num=time[0])

    if 'hours' in time and int(time[0]) > 12:
        return ':clock:'

    if 'day' in time:
        return ':triangular_flag_on_post:'

    # Replace to :facepalm:
    if 'days' in time:
        return ':space_invader:'

    return ':hourglass:'


def FormingAGoodMessage(name, last_msg, messenger):
    if 'telegram' in messenger:
        syntax = html_syntax
    if 'ryver' in messenger:
        syntax = markdown_syntax
    if 'discord' in messenger:
        syntax = discord_syntax

    not_forging_time = last_msg[name]['Not forging']
    smile = ChooseClockSmile(not_forging_time)
    message = good_msg.format(
        name=name, time=not_forging_time, smile=smile, **syntax
    )

    return message


def FormingABadMessage(i, delegates, missed_block, messenger):
    if 'telegram' in messenger:
        syntax = html_syntax
    if 'ryver' in messenger:
        syntax = markdown_syntax
    if 'discord' in messenger:
        syntax = discord_syntax

    m = []

    if missed_block:
        m.append(missed_block_string.format(**syntax))

    m.append(bad_msg.format(**syntax, **delegates[i]))
    message = ''.join(m)

    return message


def GoodMessage(name, last_msg):
    """
    Sends a message to the Ryver if delegate is forging now.
    Returns last_msg dictionary
    with delegate name and empty id of sent message.

    Sends a message to the Telegram if delegate is forging now.
    Prints a message with Telegram response for logs.

    Sends a message to the Discord if delegate is forging now.
    """

    if telegram_config['enabled']:
        message = FormingAGoodMessage(name, last_msg, 'telegram')
        tg_response = messengers.Telegram(telegram_config, message)
        print('Telegram: ', tg_response, '\n' + message + '\n')

    if ryver_config['enabled']:
        messengers.Ryver(ryver_config, last_msg[name]['id'], delete)
        message = FormingAGoodMessage(name, last_msg, 'ryver')
        messengers.Ryver(ryver_config, message)
        print('Ryver:\n' + message)

    if discord_config['enabled']:
        messengers.Discord(discord_config, last_msg[name]['id'], delete)
        message = FormingAGoodMessage(name, last_msg, 'discord')
        messengers.Discord(discord_config, message)
        print('Discord:\n' + message)


def BadMessage(last_msg, i, delegates):
    """
    Sends a message with alert to the Ryver chat.
    Prints messages for logs.
    Returns last_msg dictionary with delegate name and id of sent message.

    Sends a message with alert to the Telagram.
    Prints a message with Telegram response for logs.

    Sends a message with alert to the Discord.
    """

    name = delegates[i]['Name']
    missed_block = 'Missed block' in delegates[i]['Status']

    if telegram_config['enabled']:
        message = FormingABadMessage(i, delegates, missed_block, 'telegram')
        tg_response = messengers.Telegram(telegram_config, message)
        print('Telegram: ', tg_response, '\n' + message + '\n')

    if ryver_config['enabled']:
        message = FormingABadMessage(i, delegates, missed_block, 'ryver')
        # Deleting of the last sent message
        messengers.Ryver(ryver_config, last_msg[name]['id'], delete)
        print('Message deleted: ID_{id}\n'.format(id=last_msg[name]['id']))
        # Sending a message to the Ryver forum
        rv_response = messengers.Ryver(ryver_config, message)
        print('Ryver:\n' + message)
        # Saving an ID of the sent message
        last_msg[name]['id'] = json.loads(rv_response.text)['d']['id']

    if discord_config['enabled']:
        message = FormingABadMessage(i, delegates, missed_block, 'discord')
        # Deleting of the last sent message
        if last_msg[name]['id']:
            messengers.Discord(discord_config, last_msg[name]['id'], delete)
            print('Message deleted: ID_{id}\n'.format(id=last_msg[name]['id']))
        dc_response = messengers.Discord(discord_config, message)

        try:
            last_msg[name]['id'] = json.loads(dc_response.text)['id']
        except:
            last_msg[name]['timer'] = 0
            msg = ('Discord Message Not Sent: ' + str(dc_response))
            TelegramDebug(msg, 'Error')

        print('Discord:\n' + message)

    return last_msg


def TelegramDebug(message, m_type, disable_notification=True):
    """
    Sends all messages to Telegram even it's fake messages without any delay.
    Returns a message for logs.
    """

    tg_config = telegram_debug

    if m_type == 'Alert':
        tg_config = telegram_config

    log = '\n{type}: \n{msg}'.format(type=m_type, msg=message)

    if telegram_debug['enabled']:
        # tg_mgs = message.split('Exception: ')[1]
        tg_response = messengers.Telegram(tg_config, log, None, disable_notification)
        print('Telegram: ', tg_response, '\n' + log + '\n')
    else:
        print(log)


def explorersBadMessage(
        last_msg, url, url_mirror, explorer_online, explorer_mirror_online
        ):

    if telegram_config['enabled']:
        message = formingExplorersMessage(
            url, url_mirror, explorer_online, explorer_mirror_online,
            'telegram'
            )
        tg_response = messengers.Telegram(telegram_config, message)
        print('Telegram: ', tg_response, '\n' + message + '\n')

    if ryver_config['enabled']:
        message = formingExplorersMessage(
            url, url_mirror, explorer_online, explorer_mirror_online,
            'ryver'
            )
        # Deleting of the last sent message
        messengers.Ryver(ryver_config, last_msg['explorers']['id'], delete)
        print(
            'Message deleted: ID_{id}\n'.format(id=last_msg['explorers']['id'])
        )
        # Sending a message to the Ryver forum
        rv_response = messengers.Ryver(ryver_config, message)
        print('Ryver:\n' + message)
        # Saving an ID of the sent message
        last_msg['explorers']['id'] = json.loads(rv_response.text)['d']['id']

    if discord_config['enabled']:
        message = formingExplorersMessage(
            url, url_mirror, explorer_online, explorer_mirror_online,
            'discord'
            )
        messengers.Discord(discord_config, message)
        print('Discord:\n' + message)

    return last_msg


def explorersGoodMessage(
        last_msg, url, url_mirror, explorer_online, explorer_mirror_online
        ):

    last_msg['explorers']['online'] = True
    last_msg['explorers']['timer'] = 0

    if telegram_config['enabled']:
        message = formingExplorersMessage(
            url, url_mirror, explorer_online, explorer_mirror_online,
            'telegram', good=True
            )
        tg_response = messengers.Telegram(telegram_config, message)
        print('Telegram: ', tg_response, '\n' + message + '\n')

    if ryver_config['enabled']:
        message = formingExplorersMessage(
            url, url_mirror, explorer_online, explorer_mirror_online, 'ryver',
            good=True
            )
        messengers.Ryver(ryver_config, last_msg['explorers']['id'], delete)
        messengers.Ryver(ryver_config, message)
        print('Ryver:\n' + message)

    if discord_config['enabled']:
        message = formingExplorersMessage(
            url, url_mirror, explorer_online, explorer_mirror_online,
            'discord', good=True
            )
        messengers.Discord(discord_config, message)
        print('Discord:\n' + message)

    return last_msg


def formingExplorersMessage(
        url, url_mirror, explorer_online, explorer_mirror_online, messenger,
        good=False
        ):

    if 'telegram' in messenger:
        syntax = html_syntax
    if 'ryver' in messenger:
        syntax = markdown_syntax
    if 'discord' in messenger:
        syntax = discord_syntax

    message = message_explorers.format(
            url=url, status=explorer_online, url_mirror=url_mirror,
            status_mirror=explorer_mirror_online, **syntax
        )

    if good:
        message = message.replace(' not', '')

    return message


def forgersMessage(delegate_name, direction):
    """
    Sends a message to the Ryver, Telegram and Discord
    if delegate is IN or OUT of 101.
    """

    if direction == 'out':
        message = (
            '{out} {bold}{delegate}{bold_close}'
            ' is {bold}OUT{bold_close} of 101'
        )

    if direction == 'in':
        message = (
            '{in} {bold}{delegate}{bold_close} is {bold}IN{bold_close} 101'
        )

    if telegram_config['enabled']:
        tg_message = message.format(delegate=delegate_name, **html_syntax)
        tg_response = messengers.Telegram(telegram_config, tg_message)
        print('Telegram: ', tg_response, '\n' + tg_message + '\n')

    if ryver_config['enabled']:
        ryv_message = message.format(delegate=delegate_name, **markdown_syntax)
        messengers.Ryver(ryver_config, ryv_message)
        print('Ryver:\n' + ryv_message)

    if discord_config['enabled']:
        dis_message = message.format(delegate=delegate_name, **discord_syntax)
        messengers.Discord(discord_config, dis_message)
        print('Discord:\n' + dis_message)


def ChangeTitle(number):

    message = 'Not Forging: {number}'.format(number=number)

    resp = messengers.Discord_channel_data(discord_config, message)

    print('\n Discord title: ' + str(resp))
