# Copyright (c) 2018-2019 Mx (Shift Project delegate / 4446910057799968777S)
# Licensed under MIT License <see LICENSE file>

import time
import json

from data import config

timeout = config.timeout
threshold = config.threshold


def OrangeAndRed(delegates_table):
    """
    Sorts delegates from delegates table with 'Not forging'
    and 'Missed block' statuses.

    'STATUS': 'CIRCLE' =>
    "Forging": "green", "Awaiting slot (ok)": "green".
    "Awaiting slot (missed block)": "orange", "Missed block": "orange".
    "Not forging": "red".
    """

    delegates_sorted = {}

    for i in delegates_table:
        not_forging = 'Not forging' in delegates_table[i]['Status']
        missed_block = 'Missed block' in delegates_table[i]['Status']

        if not_forging or missed_block:
            delegates_sorted[i] = delegates_table[i]

    return delegates_sorted


def RedAndOrangeNames(delegates):
    red_and_orange_names = []

    for i in delegates:
        red_and_orange_names.append(delegates[i]['Name'])

    return red_and_orange_names


def isFake(i, delegates, delegates_mirror):
    """
    Checks a delegate's info to be shure it's not a bug.
    Sometimes explorer shows delegates_table as "Missed block"
    or "Not forging" when it's not.
    """

    if i not in delegates_mirror:
        return True

    last_block_time = lastBlockTime(i, delegates)

    if 'seconds' in last_block_time:
        return True

    if 'minute' in last_block_time:
        return True

    if 'minutes' in last_block_time and int(last_block_time[0]) < 35:
        return True

    return False


def TimeStamp():
    """
    Prints timestamp line and returns time of script's start.
    """

    start_time = time.perf_counter()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    timestamp_line = ('\n{:+^72}\n'.format(' '+str(timestamp)+' '))
    print(timestamp_line)

    return start_time


def Username(i, delegates, usernames):
    """
    Returns delegates dictionary with username of delegate
    from usernames.json file.
    """
    name = delegates[i]['Name']

    if name in usernames:
        delegates[i]['Username'] = usernames[name]
    else:
        delegates[i]['Username'] = ('NEWBIE')
    return delegates


def Timeout(last_msg, i, delegates, fake):
    """
    Returns boolean with delay and last_msg dictionary.
    Delay is True if timer of a delegate is not equal '0'.
    """

    name = delegates[i]['Name']
    missed_block = 'Missed block' in delegates[i]['Status']
    next_turn_time = delegates[i]['NextTurn'].split(' ')
    last_block_time = lastBlockTime(i, delegates)

    if not fake:
        delay = False

        if name not in last_msg:
            last_msg[name] = {}
            last_msg[name]['id'] = ''
            last_msg[name]['timer'] = 0

        if last_msg[name]['timer'] > 0:
            delay = True
            last_msg[name]['timer'] -= 1
        else:
            if not missed_block:
                # Adding a delay for messages with next turn lower threshold
                if int(next_turn_time[0]) <= threshold:
                    delay = True
                elif 'sec' == next_turn_time[1]:
                    delay = True
                else:
                    last_msg[name]['timer'] = timeout
            else:
                last_msg[name]['timer'] = timeout

        # Adding a data with not forging time for the good message
        non_f_time = last_block_time
        non_f_time.remove('ago')
        last_msg[name]['Not forging'] = ' '.join(non_f_time)

    if fake:
        delay = True

        # if name in last_msg:
        #     last_msg[name]['timer'] = 0

    return delay, last_msg


def Finished(start_time):
    """
    Returns string with time of script running atm.
    """

    finished = (
        'Finished in ~' + str(round(time.perf_counter() - start_time, 1)) +
        ' seconds'
    )

    return finished


def Logs(delegates, delegates_mirror, start_time, last_msg):
    """
    Forms a log message.
    """

    m_d = []
    m_d.append('Delegates:\n' + str(delegates) + '\n\n')
    m_d.append('Delegates mirror:\n' + str(delegates_mirror) + '\n\n')
    finished = Finished(start_time)
    m_d.append('Last msg:\n' + json.dumps(last_msg) + '\n\n')
    m_d.append(finished)
    message_debug = ''.join(m_d)

    return message_debug


def Ping(host):
    from platform import system as system_name  # Returns the system/OS name
    from subprocess import call as system_call  # Execute a shell command

    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP)
    request even if the host name is valid.
    """

    if 'http' in host:
        host = host.split('//')[1]

    if '/' in host:
        host = host.split('/')[0]

    # Ping command count option as function of OS
    param = '-n' if system_name().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    # Pinging
    return system_call(command, stdout=False) == 0


def isOnline(url, attempts, pause):
    """
    Returns True if url responds to a ping request.
    And False if url is not responds after range of attempts.
    After every False attempt it waits for a pause.
    """

    for _ in range(attempts):
        ping = Ping(url)

        if ping:
            return True
        else:
            time.sleep(pause)

    return False


def explorersTimeout(last_msg, delay=False):
    """
    Returns last_msg file and delay.
    Delay is True if 'timer > 0'.
    If 'timer <= 0' dalay is False and sets a timeout.
    """

    if 'explorers' not in last_msg:
        last_msg['explorers'] = {}
        last_msg['explorers']['timer'] = 0

    if last_msg['explorers']['timer'] > 0:
        delay = True
        last_msg['explorers']['timer'] -= 1
    else:
        last_msg['explorers']['timer'] = timeout

    return last_msg, delay


def lastBlockTime(i, delegates):
    last_block_time = delegates[i]['lastBlockTime'].split(' ')

    return last_block_time
