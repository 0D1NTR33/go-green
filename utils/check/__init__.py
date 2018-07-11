def OrangeAndRed(delegates_table):
    """
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
