import json
# import utils.send.messengers as messengers


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


def RyverGoodMessage(ryver_config, name, good_msg, last_msg):
    delete = True

    if ryver_config['enabled']:
        messengers.Ryver(ryver_config, last_msg[name]['id'], delete)
        last_msg[name]['id'] = ''

        good_msg = (
            '**{name}** is forging now! :white_check_mark:'
            .format(name=name)
        )
        messengers.Ryver(ryver_config, good_msg)
        print('Ryver:\n' + good_msg)

    return last_msg


def TelegramGoodMessage(telegram_config, good_msg):
    if telegram_config['enabled']:
        tg_response = messengers.Telegram(telegram_config, good_msg)
        print('Telegram: ', tg_response, '\n')