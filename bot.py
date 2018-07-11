# Copyright (c) 2018 Mx (Shift Project delegate / 4446910057799968777S)
# Licensed under MIT License <see LICENSE file>

import json
from os import path

import utils.check as check
import utils.get.parser as get
import utils.send as send
from data import config

start_time = check.TimeStamp()

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

url = config.explorer[0]
url_mirror = config.explorer[1]
max_attempts = 10

""" Main script """

delegates = get.DelegatesRedAndOrange(url, max_attempts)
delegates_mirror = get.DelegatesRedAndOrange(url_mirror, max_attempts)

for i in delegates:
    message = ''
    delay = True

    not_forging = 'Not forging' in delegates[i]['Status']
    missed_block = 'Missed block' in delegates[i]['Status']
    name = delegates[i]['Name']

    # Checking for a fake message
    fake = False

    if not_forging or missed_block:
        delegates = check.Username(i, name, delegates, usernames)
        last_block_time = delegates[i]['lastBlockTime'].split(' ')
        next_turn_time = delegates[i]['NextTurn'].split(' ')

        fake = check.isFake(i, delegates_mirror, last_block_time)

    # Adding a delay for recurring messages for delegate
        delay, last_msg = check.Timeout(
            last_msg, name, fake, last_block_time, next_turn_time
        )
    # Reset the timer if delegate is forging now and send a good message
    else:
        if name in last_msg:
            last_msg[name]['timer'] = 0

            if last_msg[name]['Not forging']:
                last_msg = send.GoodMessage(name, last_msg)

    # Finally forming and sending a message
    if (not_forging or missed_block) and not delay:
        last_msg = send.BadMessage(name, last_msg, i, delegates, missed_block)

# Saving last messages to a file
with open(last_msg_path, mode='w', encoding='utf-8') as f:
    json.dump(last_msg, f)

# Logs
message_debug = check.Logs(delegates, delegates_mirror, start_time)
send.TelegramDebug(message_debug)
print('\nDebug:\n' + message_debug)
