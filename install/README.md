# GoGreen bot v 0.1.8
## Installation Guide

1. Clone this repository to your server:
```
git clone https://github.com/MxShift/go-green.git
```

2. Go to the install derectory:
```
cd go-green && cd install
```

3. Install all dependencies:
```
bash install.sh
```

4. Start Selenium Server in the background:
```
screen -R selenium
bash ./selenium-server.sh start-chrome
```
> Then press `CTRL + A + D`

5. Change `data/config.py` file with your settings.

6. Setup a cron:
```
crontab -e
```
> Copy and paste:
```
# Start GoGreen Bot every 15 minutes
*/15 * * * * python3 ~/go-green/bot.py >> ~/go-green/bot.log 2>&1
```

7. Enjoy! :tada: