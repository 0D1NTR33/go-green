# -*- coding: utf-8 -*-

# import sys
import time
import json
from os import path

import get
from send import messengers as send

timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
print('\n{:+^72}\n'.format(' '+str(timestamp)+' '))

dir = path.abspath(path.dirname(__file__))

config_path = path.join(dir, 'data', 'config.json')
usernames_path = path.join(dir, 'data', 'usernames.json')

with open(config_path, 'r') as f:
    config = json.load(f)

with open(usernames_path, 'r') as f:
    usernames = json.load(f)

telegram_config = config["telegram"]
ryver_config = config["ryver"]

url = config["explorer"]
max_attempts = 100

delegates = get.table.Delegates(url, max_attempts)

# 'STATUS': 'CIRCLE' => "Forging": "green", "Awaiting slot (ok)": "green";
# "Awaiting slot (missed block)": "orange", "Missed block": "orange";
# "Not forging": "red";
m = []
for i in delegates:
    not_forging = 'red' in delegates[i]['Circle']
    missed_block = 'orange' in delegates[i]['Circle']

    if not_forging or missed_block:
        if delegates[i]['Name'] in usernames:
            delegates[i]['Username'] = usernames[delegates[i]['Name']]
        else:
            delegates[i]['Username'] = ('_Please send '
                                        'your Ryver username to me_')
        m.append(
            'Delegate: **{Name}** / @{Username}\nLast block forged: '
            '**{lastBlockTime}**\n**Next turn:** {ForgingTime}\n\n'
            .format(**delegates[i])
        )

message = ''.join(m)

if ryver_config['enabled']:
    # Checking if message is not empty
    if message:
        send.Ryver(message, ryver_config)

if telegram_config['enabled']:
    if message:
        send.Telegram(message, telegram_config)

# Printing message for logs
print(message)
