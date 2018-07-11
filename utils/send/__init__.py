import json
from utils.send import messengers

good_msg = '**{name}** is forging now! :white_check_mark:'


def RyverBadMessage(ryver_config, name, message, last_msg):
    delete = True

    if ryver_config['enabled']:
        # Deleting of the last sent message
        messengers.Ryver(ryver_config, last_msg[name]['id'], delete)
        print('Message deleted: ID_{id}\n'.format(id=last_msg[name]['id']))
        # Sending a message to the Ryver forum
        rv_response = messengers.Ryver(ryver_config, message)
        print('Ryver:\n' + message)
        # Saving an ID of the sent message
        last_msg[name]['id'] = json.loads(rv_response.text)['d']['id']

    return last_msg


def TelegramBadMessage(telegram_config, message):
    if telegram_config['enabled']:
        tg_response = messengers.Telegram(telegram_config, message)
        print('Telegram: ', tg_response, '\n')


def RyverGoodMessage(ryver_config, name, last_msg):
    delete = True

    if ryver_config['enabled']:
        messengers.Ryver(ryver_config, last_msg[name]['id'], delete)
        last_msg[name]['id'] = ''
        message = good_msg.format(name=name)
        messengers.Ryver(ryver_config, message)
        print('Ryver:\n' + good_msg)

    return last_msg


def TelegramGoodMessage(telegram_config, name):
    if telegram_config['enabled']:
        message = good_msg.format(name=name)
        tg_response = messengers.Telegram(telegram_config, message)
        print('Telegram: ', tg_response, '\n')


def TelegramDebug(telegram_debug, m_d, finished):
    debug_message = ''

    if telegram_debug['enabled']:
        m_d.append(finished)
        debug_message = ''.join(m_d)
        messengers.Telegram(telegram_debug, debug_message)

    return debug_message
