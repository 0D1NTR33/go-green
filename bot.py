# -*- coding: utf-8 -*-

# import sys
import time
import json
from os import path

from data import config as config
from get import parser as get
from send import messengers as send

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
    last_msg = {'id': 'None'}
    with open(last_msg_path, 'r', encoding='utf-8') as f:
        last_msg['id'] = json.load(f)['id']
except:
    pass

telegram_config = config.telegram
ryver_config = config.ryver

url = config.explorer[0]
max_attempts = 10

delegates = get.Delegates(url, max_attempts)

# 'STATUS': 'CIRCLE' => "Forging": "green", "Awaiting slot (ok)": "green".
# "Awaiting slot (missed block)": "orange", "Missed block": "orange".
# "Not forging": "red".
m = []
for i in delegates:
    """
    "Missed blocks" status disabled because of erroneous messages.
    """
    not_forging = 'red' in delegates[i]['Circle']
    # missed_block = 'orange' in delegates[i]['Circle']

    # if not_forging or missed_block:
    if not_forging:
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
            '**Next turn:** {ForgingTime}\n\n'
            .format(**delegates[i])
        )

message = ''.join(m)
delete = True

if ryver_config['enabled']:
    # Deleting of the last sent message
    send.Ryver(ryver_config, last_msg['id'], delete)
    print('Message deleted: ID_{id}\n'.format(id=last_msg['id']))
    # Checking if message is not empty
    if message:
        # Sending a message to the Ryver forum
        response = send.Ryver(ryver_config, message)
        # Saving to a file ID of the sent message
        last_msg['id'] = json.loads(response)['d']['id']

        with open(last_msg_path, mode='w', encoding='utf-8') as f:
            json.dump(last_msg, f)

if telegram_config['enabled']:
    if message:
        send.Telegram(telegram_config, message)

# Printing a message for logs
print(message)

finished = (
    'Finished in ' + str(round(time.perf_counter() - start_time, 1)) +
    ' seconds'
)
print(finished)
