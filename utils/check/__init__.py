def OrangeAndRed(delegates_table):
    """
    Sorting delegates from delegates table with 'Not forging'
    and 'Missed block' status.

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
    Checking a delegate's info to be shure it's not a bug.
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
