# -*- coding: utf-8 -*-

import time
import json
from os import path

import get.parser as get
import send.messengers as send
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

        if 'id' not in last_msg:
            last_msg['id'] = '0'

        if 'red' not in last_msg:
            last_msg['red'] = {}

        if 'timer' not in last_msg:
            last_msg['timer'] = 0
except:
    pass
# Ticking the timer
last_msg['timer'] += 1

telegram_config = config.telegram
ryver_config = config.ryver
counter = config.counter
timeout = config.timeout

url = config.explorer[0]
max_attempts = 10

delegates = {}
delegates = get.Delegates(url, max_attempts)
# delegates = {
#     1: {
#         'NextTurn': '41 min 51 sec',
#         'lastBlockTime': '45 minutes ago',
#         'Name': 'mrgr',
#         'Circle': '<i class="forging-status fa fa-circle red"'
#     },
#     2: {
#         'NextTurn': '41 min 51 sec',
#         'lastBlockTime': '46 minutes ago',
#         'Name': 'lol',
#         'Circle': '<i class="forging-status fa fa-circle red"'
#     }
# }

"""
'STATUS': 'CIRCLE' =>
"Forging": "green", "Awaiting slot (ok)": "green".
"Awaiting slot (missed block)": "orange", "Missed block": "orange".
"Not forging": "red".
"""
m = []
for i in delegates:
    """
    "Missed blocks" status disabled because of erroneous messages.
    """
    not_forging = 'red' in delegates[i]['Circle']
    missed_block = 'orange' in delegates[i]['Circle']
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

    # Double-checking of messages with a counter
        if not fake:
            fake = True

            if name in last_msg['red']:
                last_msg['red'][name] += 1
            else:
                last_msg['red'][name] = 1

            time_to_send = (
                last_msg['timer'] > timeout and
                last_msg['red'][name] >= counter
            )

            if time_to_send:
                fake = False
                last_msg['red'][name] = 0
    # If status is 'Forging': reset the counter
    else:
        if name in last_msg['red']:
            last_msg['red'][name] = 0

    # Finally forming a message
    if not_forging and not fake:
        if delegates[i]['Name'] in usernames:
            delegates[i]['Username'] = usernames[delegates[i]['Name']]
        else:
            delegates[i]['Username'] = ('_Please send '
                                        'your Ryver username to_ @mx')
        # if missed_block:
        #     m.append('_Missed block_\n')

        m.append(
            'Delegate: **{Name}** / @{Username}\n'
            'Last block forged: **{lastBlockTime}**\n'
            '**Next turn:** {NextTurn}\n\n'
            .format(**delegates[i])
        )

message = ''.join(m)
delete = True

if ryver_config['enabled']:
    # Checking if message is not empty
    if message:
        # Deleting of the last sent message
        send.Ryver(ryver_config, last_msg['id'], delete)
        print('Message deleted: ID_{id}\n'.format(id=last_msg['id']))
        # Sending a message to the Ryver forum
        rv_response = send.Ryver(ryver_config, message)
        # Saving an ID of the sent message
        last_msg['id'] = json.loads(rv_response.text)['d']['id']

# Reset the timer
if last_msg['timer'] > timeout:
    last_msg['timer'] = 0

# Saving last messages to a file
with open(last_msg_path, mode='w', encoding='utf-8') as f:
    json.dump(last_msg, f)

finished = (
    'Finished in ~' + str(round(time.perf_counter() - start_time, 1)) +
    ' seconds'
)

if telegram_config['enabled']:
    if telegram_config['debug']:
        m.append(finished)
        message = ''.join(m)
    if message:
        tg_response = send.Telegram(telegram_config, message)
        print('Telegram: ', tg_response, '\n')
        last_msg['timer'] = 0

# Printing a messages for logs
print(message)

if not telegram_config['debug']:
    print(finished)
