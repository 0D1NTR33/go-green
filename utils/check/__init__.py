# Copyright (c) 2018 Mx (Shift Project delegate / 4446910057799968777S)
# Licensed under MIT License <see LICENSE file>

import time

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


def isFake(i, delegates_mirror, last_block_time):
    """
    Checks a delegate's info to be shure it's not a bug.
    Sometimes explorer shows delegates_table as "Missed block"
    or "Not forging" when it's not.
    """

    if 'seconds' in last_block_time:
        return True

    if 'minute' in last_block_time:
        return True

    if 'minutes' in last_block_time and int(last_block_time[0]) < 45:
        return True

    if i not in delegates_mirror:
        return True

    return False


def TimeStamp():
    """
    Prints timestamp line and returns time of script's start
    """

    start_time = time.perf_counter()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    timestamp_line = ('\n{:+^72}\n'.format(' '+str(timestamp)+' '))
    print(timestamp_line)

    return start_time


def Username(i, name, delegates, usernames):
    """
    Returns delegates dictionary with username of delegate
    from usernames.json file.
    """

    if name in usernames:
        delegates[i]['Username'] = usernames[name]
    else:
        delegates[i]['Username'] = ('_Please send '
                                    'your Ryver username to_ @mx')
    return delegates


def Timeout(last_msg, name, fake, last_block_time, next_turn_time):
    """
    Returns boolean with delay and last_msg dictionary.
    Delay is True if timer of a delegate is not equal '0'.
    """

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
            if int(next_turn_time[0]) <= threshold:
                delay = True
            elif 'sec' == next_turn_time[1]:
                delay = True
            else:
                last_msg[name]['timer'] = timeout

        # Adding a data with not forging time for the good message
        non_f_time = last_block_time
        non_f_time.remove('ago')
        last_msg[name]['Not forging'] = ' '.join(non_f_time)

    else:
        delay = True

        if name in last_msg:
            last_msg[name]['timer'] = 0

    return delay, last_msg


def Finished(start_time):
    """
    Returns string with time of script running atm
    """

    finished = (
        'Finished in ~' + str(round(time.perf_counter() - start_time, 1)) +
        ' seconds'
    )

    return finished


def Logs(delegates, delegates_mirror, start_time):
    m_d = []
    m_d.append('Delegates:\n' + str(delegates) + '\n\n')
    m_d.append('Delegates mirror:\n' + str(delegates_mirror) + '\n\n')
    finished = Finished(start_time)
    m_d.append(finished)
    message_debug = ''.join(m_d)

    return message_debug
