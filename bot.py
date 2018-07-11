# -*- coding: utf-8 -*-

import time
import json
from os import path

import utils.check as check
import utils.get.parser as get
import utils.send.messengers as send
from data import config

start_time = time.perf_counter()
timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
timestamp_line = ('\n{:+^72}\n'.format(' '+str(timestamp)+' '))
print(timestamp_line)

dir = path.abspath(path.dirname(__file__))

usernames_path = path.join(dir, 'data', 'usernames.json')
last_msg_path = path.join(dir, 'data', 'last_msg.json')

with open(usernames_path, 'r', encoding='utf-8') as f:
    usernames = json.load(f)

# Trying to open last_msg.json file even it's empty
try:
    last_msg = {}
    with open(last_msg_path, 'r', encoding='utf-8') as f:
        last_msg = json.load(f)
except:
    pass
finally:
    if 'id' not in last_msg:
        last_msg['id'] = '0'

    if 'timer' not in last_msg:
        last_msg['timer'] = {}

telegram_config = config.telegram
telegram_debug = config.telegram_debug
ryver_config = config.ryver

counter = config.counter
timeout = config.timeout

url = config.explorer[0]
url_mirror = config.explorer[1]
max_attempts = 10

delegates_table = {}
delegates = {}
delegates_table_mirror = {}
delegates_mirror = {}

delegates = get.Delegates_table(url, max_attempts)
delegates_table_mirror = get.Delegates_table(url_mirror, max_attempts)

delegates_mirror = check.OrangeAndRed(delegates_table_mirror)

m = []
m_d = []
for i in delegates:
    not_forging = 'Not forging' in delegates[i]['Status']
    missed_block = 'Missed block' in delegates[i]['Status']
    name = delegates[i]['Name']

    # Checking for a fake message
    fake = False
    if not_forging or missed_block:
        last_block_time = delegates[i]['lastBlockTime'].split(' ')

        if 'seconds' in last_block_time:
            fake = True

        if 'minute' in last_block_time:
            fake = True

        if 'minutes' in last_block_time and int(last_block_time[0]) < 45:
            fake = True

        if i not in delegates_mirror:
            fake = True

    # Adding a delay for recurring messages for delegate
        if not fake:
            if name not in last_msg['timer']:
                last_msg['timer'][name] = 0

            if last_msg['timer'][name] > 0:
                last_msg['timer'][name] -= 1
                fake = True
            else:
                last_msg['timer'][name] = timeout
        else:
            if name in last_msg['timer']:
                last_msg['timer'][name] = 0
    # Reset the timer if delegate is forging
    else:
        if name in last_msg['timer']:
            last_msg['timer'][name] = 0

    # Finally forming a message
    if (not_forging or missed_block) and not fake:
        if delegates[i]['Name'] in usernames:
            delegates[i]['Username'] = usernames[delegates[i]['Name']]
        else:
            delegates[i]['Username'] = ('_Please send '
                                        'your Ryver username to_ @mx')
        if missed_block:
            m.append('_Missed block_\n')

        m.append(
            'Delegate: **{Name}** / @{Username}\n'
            'Last block forged: **{lastBlockTime}**\n'
            '**Next turn:** {NextTurn}\n\n'
            .format(**delegates[i])
        )

    # Forming a message for Telegram logs
    if telegram_debug['enabled']:
        if not_forging or missed_block:
            if missed_block:
                m_d.append('<i>Missed block</i>\n')

            m_d.append(
                'Delegate: <b>{Name}</b>\n'
                'Last block forged: <b>{lastBlockTime}</b>\n'
                '<b>Next turn:</b> {NextTurn}\n\n'
                .format(**delegates[i])
            )

message = ''.join(m)
delete = True

if ryver_config['enabled']:
    # Checking if message is not empty
    if message:
        # Deleting of the last sent message
        # send.Ryver(ryver_config, last_msg['id'], delete)
        print('Message deleted: ID_{id}\n'.format(id=last_msg['id']))
        # Sending a message to the Ryver forum
        rv_response = send.Ryver(ryver_config, message)
        # Saving an ID of the sent message
        last_msg['id'] = json.loads(rv_response.text)['d']['id']

if telegram_config['enabled']:
    if message:
        tg_response = send.Telegram(telegram_config, message)
        print('Telegram: ', tg_response, '\n')

# Saving last messages to a file
with open(last_msg_path, mode='w', encoding='utf-8') as f:
    json.dump(last_msg, f)

finished = (
    'Finished in ~' + str(round(time.perf_counter() - start_time, 1)) +
    ' seconds'
)

if telegram_debug['enabled']:
    m_d.append(finished)
    debug_message = ''.join(m_d)
    send.Telegram(telegram_debug, debug_message)

# Printing a messages for logs
print('Ryver:\n' + message)

if telegram_debug['enabled']:
    print('Debug:\n' + debug_message)
else:
    print(finished)
