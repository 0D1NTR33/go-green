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
Please be sure that you type 'True' or 'False' with a capital letter.
Also, it shouldn't have any type of brackets.
"""
# Telegram bot data
telegram = {
    "enabled": True,
    "debug": True,
    "apiKey": "",
    "chat_id": ""
}

# Ryver data
ryver = {
    "enabled": True,
    "projectName": "shiftnrg",
    "forumID": "1094320",
    "login": "",
    "password": ""
}
