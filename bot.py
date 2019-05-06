# Copyright (c) 2018-2019 Mx (Shift Project delegate / 4446910057799968777S)
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
ACTIVE_DELEGATES_PATH = path.join(DIR_PATH, 'data', 'active_delegates.json')

with open(USERNAMES_PATH, 'r', encoding='utf-8') as f:
    usernames = json.load(f)

# Trying to open last_msg.json file even it's empty
try:
    last_msg = {}
    with open(LAST_MSG_PATH, 'r', encoding='utf-8') as f:
        last_msg = json.load(f)
except:
    pass

# Trying to open active_delegates.json file even it's empty
try:
    previous_active_delegates = {}
    with open(ACTIVE_DELEGATES_PATH, 'r', encoding='utf-8') as f:
        previous_active_delegates = json.load(f)
except:
    pass

url = config.explorer[0]
url_mirror = config.explorer[1]
timeout = config.timeout

max_attempts = 4

""" Main script """

try:
    # Scraping delegates info
    (
        delegates, active_delegates, attempt
    ) = get.DelegatesRedAndOrange(url, max_attempts)

    (
        delegates_mirror, active_delegates_mirror, attempt_mirror
    ) = get.DelegatesRedAndOrange(url_mirror, max_attempts)

    # Checking for successful scraping
    if (attempt == max_attempts) and (attempt_mirror == max_attempts):
        raise Exception("Scraping failed")

    # Checking for explorers' online
    # Need to be improved (timer for reccuring messages, back online message)
    else:
        if attempt == max_attempts:
            message_explorer = ('Explorer is offline: ' + url)
            send.TelegramDebug(message_explorer, 'Alert', False)

        if attempt_mirror == max_attempts:
            message_explorer = ('Explorer is offline: ' + url_mirror)
            send.TelegramDebug(message_explorer, 'Alert', False)

    # Checking delegates
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

    # Adding a number of not forging or missed blocks delegates
    # to a Discord audio channel title
    send.ChangeTitle(len(last_msg))

    # Checking in and out delegates
    synchronized = (active_delegates == active_delegates_mirror)

    if previous_active_delegates and synchronized:
        for d in previous_active_delegates:
            if previous_active_delegates[d] not in active_delegates.values():
                delegate_name = previous_active_delegates[d]
                send.forgersMessage(delegate_name, 'out')

        for d in active_delegates:
            if active_delegates[d] not in previous_active_delegates.values():
                delegate_name = active_delegates[d]
                send.forgersMessage(delegate_name, 'in')

    if synchronized:
        previous_active_delegates = active_delegates

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

    # Saving active delegates to a file
    with open(ACTIVE_DELEGATES_PATH, mode='w', encoding='utf-8') as f:
        json.dump(previous_active_delegates, f)
