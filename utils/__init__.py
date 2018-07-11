def MessageForRyver(i, delegates, missed_block):
    m = []

    if missed_block:
        m.append('_Missed block_\n')

    m.append(
        'Delegate: **{Name}** / @{Username}\n'
        'Last block forged: **{lastBlockTime}**\n'
        '**Next turn:** {NextTurn}\n\n'
        .format(**delegates[i])
    )

    return ''.join(m)


def MessageForTelegram(i, delegates, m_d, missed_block):
    if missed_block:
        m_d.append('<i>Missed block</i>\n')

    m_d.append(
        'Delegate: <b>{Name}</b>\n'
        'Last block forged: <b>{lastBlockTime}</b>\n'
        '<b>Next turn:</b> {NextTurn}\n\n'
        .format(**delegates[i])
    )

    return m_d
