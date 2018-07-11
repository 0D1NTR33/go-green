""" Config file """

"""
Atm you can't check is explorer synchronised or not.
Therefore, for a double-checking uses 2 explorers.
"""
# Tuple of explorers
explorer = (
    'https://explorer.testnet.shiftnrg.org',
    'https://testnet.shiftnrg.com.mx'
)

"""
Number of active delegates on explorer's delegateMonitor page.
"""
# Number of delegates to check
active_delegates = 101

"""
Timeout '1' mean if we have a message it will be sent,
but next will be sent only on the 3-rd run of the script.

Workmode:
timeout = 23
Script running once in 15 minutes.
Recurring message will be sent every 6 hours.
"""
# Delay for recurring messages
timeout = 3

"""
'Next time turn' threshold delay for sending message.

Example:
treshold = 25
Explorer shows a delegate with 'Not forging' status.
Message will be sent only if time to next turn is greater then 25.
Hovewer, if status is 'Missed block' message will be sent anyway.

If set 45 or greater, messages for status 'Not forging' will not be sent ever.
"""
# Values between 1 and 45
threshold = 25

"""
Please be sure that you type 'True' or 'False' with a capital letter.
Also, it shouldn't have any type of brackets.
"""

"""
'apiKey' - token of your Telegram bot.
'chat_id' - ID of your Telegram chat or channel.

Bot should be an admin of chat or channel for posting messages.
Also, you can recive messages from bot itself by using as a chat_id
your own ID.

You can find your ID or ID of chat or channel by using @get_id_bot bot.
"""
# Telegram bot data for posting messages
telegram = {
    'enabled': False,
    'apiKey': '',
    'chat_id': ''
}

"""
Can be used same bot, but just another chat or channel.
"""
# Telegram bot data for logs
telegram_debug = {
    'enabled': False,
    'apiKey': '',
    'chat_id': ''
}

"""
'projectName' - name of your Ryver project.
'forumID' - ID of your Ryver forum to send messages to.
'login' - login of your bot's account.
'password' - password of your bot's account.

Bot should be added to the forum manually.
"""
# Ryver data for posting messages
ryver = {
    'enabled': False,
    'projectName': 'shiftnrg',
    'forumID': '1094320',
    'login': '',
    'password': ''
}

"""
Discord webhook url.
You can setup it in you server settings.
Server Settings -> Webhooks -> Create Webhook
"""
# Discord settings
discord = {
    'enabled': False,
    'webhook_url': ''
}
