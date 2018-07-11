"""
    Config file
"""

"""
Please be sure you haven't slash ('/') at the end of an explorer link,
because in this case a Delegate Monitor tool page can't load a data.
I guess, it's kind of a bug.
"""
# Tuple of explorers
explorer = (
    'https://explorer.testnet.shiftnrg.org/delegateMonitor',
    'https://testnet.shiftnrg.com.mx/delegateMonitor'
)

"""
Timeout '1' mean if we have a message it will be sent,
but next will be sent only on the 3-rd run of the script.

Workmode:
timeout = 7
script running once in 15 minutes
recurring message will be sent every 2 hours
"""
# Delay for recurring messages
timeout = 7

"""
Please be sure that you type 'True' or 'False' with a capital letter.
Also, it shouldn't have any type of brackets.
"""
# Telegram bot data
telegram = {
    "enabled": False,
    "apiKey": "",
    "chat_id": ""
}

# Telegram bot data
telegram_debug = {
    "enabled": False,
    "apiKey": "",
    "chat_id": ""
}

# Ryver data
ryver = {
    "enabled": False,
    "projectName": "shiftnrg",
    "forumID": "",
    "login": "",
    "password": ""
}
