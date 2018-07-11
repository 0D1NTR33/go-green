import json
from utils.send import messengers
from data import config

telegram_config = config.telegram
telegram_debug = config.telegram_debug
ryver_config = config.ryverTest
discord_config = config.discord

delete = True

markdown_syntax = {
    'bold': '**',
    'bold_close': '**',
    'italic': '_',
    'italic_close': '_'
}
html_syntax = {
    'bold': '<b>',
    'bold_close': '</b>',
    'italic': '<i>',
    'italic_close': '</i>'
}

discord_syntax = {
    'bold': '**',
    'bold_close': '**',
    'italic': '*',
    'italic_close': '*'
}

good_msg = (
    '{bold}{name}{bold_close} is now green! :white_check_mark: \n'
    'Not forging time: {bold}{time}{bold_close} {smile}'
)

missed_block_string = '{italic}Missed block{italic_close}\n'

bad_msg = (
    'Delegate: {bold}{Name}{bold_close} / @{Username}\n'
    'Last block forged: {bold}{lastBlockTime}{bold_close}\n'
    '{bold}Next turn:{bold_close} {NextTurn}\n\n'
)


def ChooseClockSmile(time):
    clock = ':clock{num}:'

    time = time.split(' ')

    if 'hour' in time:
        return clock.format(num=1)

    if 'hours' in time and int(time[0]) <= 12:
        return clock.format(num=time[0])

    if 'hours' in time and int(time[0]) > 12:
        return ':mantelpiece_clock:'

    if 'day' in time:
        return ':triangular_flag_on_post:'

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

    m.append(bad_msg.format(**delegates[i], **syntax))
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
        last_msg[name]['id'] = ''
        message = FormingAGoodMessage(name, last_msg, 'ryver')
        messengers.Ryver(ryver_config, message)
        print('Ryver:\n' + message)

    if discord_config['enabled']:
        message = FormingAGoodMessage(name, last_msg, 'discord')
        messengers.Discord(discord_config, message)

    last_msg[name]['Not forging'] = ''

    return last_msg


def BadMessage(name, last_msg, i, delegates, missed_block):
    """
    Sends a message with alert to the Ryver chat.
    Prints messages for logs.
    Returns last_msg dictionary with delegate name and id of sent message.

    Sends a message with alert to the Telagram.
    Prints a message with Telegram response for logs.

    Sends a message with alert to the Discord.
    """

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
        messengers.Discord(discord_config, message)

    return last_msg


def TelegramDebug(telegram_debug, m_d, finished):
    """
    Sends all messages to Telegram even it's fake messages without any delay.
    Returns a message for logs.
    """

    debug_message = ''

    if telegram_debug['enabled']:
        m_d.append(finished)
        debug_message = ''.join(m_d)
        messengers.Telegram(telegram_debug, debug_message)

    return debug_message
