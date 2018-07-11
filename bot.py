# Copyright (c) 2018 Mx (Shift Project delegate / 4446910057799968777S)
# Licensed under MIT License <see LICENSE file>

import json
from os import path

import utils.check as check
import utils.get.parser as get
import utils.send as send
from data import config

start_time = check.TimeStamp()

DIR_PATH = path.abspath(path.dirname(__file__))
USERNAMES_PATH = path.join(DIR_PATH, 'data', 'usernames.json')
LAST_MSG_PATH = path.join(DIR_PATH, 'data', 'last_msg.json')

with open(USERNAMES_PATH, 'r', encoding='utf-8') as f:
    usernames = json.load(f)

# Trying to open last_msg.json file even it's empty
try:
    last_msg = {}
    with open(LAST_MSG_PATH, 'r', encoding='utf-8') as f:
        last_msg = json.load(f)
except:
    pass

url = config.explorer[0]
url_mirror = config.explorer[1]
timeout = config.timeout

double_checking = True
max_attempts = 10

""" Main script """

try:
    # Checking explorers` online
    explorer_online = check.isOnline(url, 3, 5)
    explorer_mirror_online = check.isOnline(url_mirror, 3, 5)

    if 'explorers' not in last_msg:
        last_msg['explorers'] = {}
        last_msg['explorers']['online'] = True

    if double_checking and (not explorer_online or not explorer_mirror_online):

        last_msg, delay = check.explorersTimeout(last_msg)
        last_msg['explorers']['online'] = False

        if not delay:
            send.explorersBadMessage(
                last_msg, url, url_mirror, explorer_online,
                explorer_mirror_online
            )

        message_explorers = send.formingExplorersMessage(
            url, url_mirror, explorer_online, explorer_mirror_online,
            'telegram',
        )
        send.TelegramDebug(message_explorers, 'Explorers')

        # Saving data to a file
        with open(LAST_MSG_PATH, mode='w', encoding='utf-8') as f:
            json.dump(last_msg, f)

        # Exit from the script
        raise SystemExit

    # Sending a good message if both explorers is online now
    if not last_msg['explorers']['online']:
        last_msg = send.explorersGoodMessage(
                last_msg, url, url_mirror, explorer_online,
                explorer_mirror_online
            )

    # Checking delegates
    delegates = get.DelegatesRedAndOrange(url, max_attempts)
    delegates_mirror = get.DelegatesRedAndOrange(url_mirror, max_attempts)

    for i in delegates:
        delay = True
        fake = False

        # Checking for a fake message
        fake = check.isFake(i, delegates, delegates_mirror)

        # Adding a delay for recurring messages for a delegate
        delay, last_msg = check.Timeout(last_msg, i, delegates, fake)

        # Finally forming and sending a message
        if not delay:
            delegates = check.Username(i, delegates, usernames)
            last_msg = send.BadMessage(last_msg, i, delegates)

    # Send a good message if delegate is forging now and delete from last_msg
    red_and_orange_names = check.RedAndOrangeNames(delegates)
    red_and_orange_names_mirror = check.RedAndOrangeNames(delegates_mirror)

    to_del = []
    for n in last_msg:
        if n == 'explorers':
            continue

        delegate_is_forging_now = (
            n not in red_and_orange_names and
            n not in red_and_orange_names_mirror
        )

        if delegate_is_forging_now:
            to_del.append(n)
            send.GoodMessage(n, last_msg)

    for n in to_del:
        del last_msg[n]

    # Logs
    message_debug = check.Logs(
        delegates, delegates_mirror, start_time, last_msg
    )
    send.TelegramDebug(message_debug, 'Log')
except Exception:
    import traceback

    message_error = traceback.format_exc()
    send.TelegramDebug(message_error, 'Error')
finally:
    # Saving last messages to a file
    with open(LAST_MSG_PATH, mode='w', encoding='utf-8') as f:
        json.dump(last_msg, f)
