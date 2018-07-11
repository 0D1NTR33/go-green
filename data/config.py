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
Double-checking to totally avoid fake messages.
If sets '2' it mean a message will be sent only if
delegate has the same status two times in a row.
If delegate has status 'Not forging' and script has launched 2 times
and both iterations status has been the same a message will be sent.
Otherwise bot resets the counter.
Also, bot resets the counter after each sent message.
"""
# Counter for a double-checking messages
counter = 2

"""
If timeout '1' it means if we have a message
it will be sent only on the 2-nd run of the script.
Workmode:
timeout = 7
script running once in 15 minutes
messege will be sent every 2 hours
"""
# Here a comment for timeout
timeout = 7

"""
Please be sure that you type 'True' or 'False' with a capital letter.
Also, it shouldn't have any type of brackets.
"""
# Telegram bot data
telegram = {
    "enabled": False,
    "debug": False,
    "apiKey": "",
    "chat_id": ""
}

# Ryver data
ryver = {
    "enabled": False,
    "projectName": "shiftnrg",
    "forumID": "1094320",
    "login": "",
    "password": ""
}