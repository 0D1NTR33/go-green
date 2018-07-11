# -*- coding: utf-8 -*-

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

telegram_debug = config.telegram_debug

url = config.explorer[0]
url_mirror = config.explorer[1]
max_attempts = 10

delegates = {}
delegates_table_mirror = {}
delegates_mirror = {}

"""
    Main script
"""

delegates = get.Delegates_table(url, max_attempts)
delegates_table_mirror = get.Delegates_table(url_mirror, max_attempts)

delegates_mirror = check.OrangeAndRed(delegates_table_mirror)

m_d = []

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

        fake = check.isFake(i, delegates_mirror, last_block_time)

    # Adding a delay for recurring messages for delegate
        delay, last_msg = check.Timeout(
            last_msg, name, fake, last_block_time
        )
    # Reset the timer if delegate is forging now and send a good message
    else:
        if name in last_msg:
            last_msg[name]['timer'] = 0

            if last_msg[name]['id']:
                last_msg = send.GoodMessage(name, last_msg)

    # Finally forming and sending a message
    if (not_forging or missed_block) and not delay:
        last_msg = send.BadMessage(name, last_msg, i, delegates, missed_block)

    # Forming a message for Telegram logs
    if telegram_debug['enabled']:
        if not_forging or missed_block:
            m_d.append(
                send.FormingABadMessage(i, delegates, missed_block, 'telegram')
            )

# Saving last messages to a file
with open(last_msg_path, mode='w', encoding='utf-8') as f:
    json.dump(last_msg, f)

finished = check.Finished(start_time)
message_debug = send.TelegramDebug(telegram_debug, m_d, finished)

# Printing a messages for logs
if telegram_debug['enabled']:
    print('\nDebug:\n' + message_debug)
else:
    print(finished)
