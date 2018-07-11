#!/usr/bin/env bash
# https://developers.supportbee.com/blog/setting-up-cucumber-to-run-with-Chrome-on-Linux/
# https://gist.github.com/curtismcmullan/7be1a8c1c841a9d8db2c
# http://stackoverflow.com/questions/10792403/how-do-i-get-chrome-working-with-selenium-using-php-webdriver
# http://stackoverflow.com/questions/26133486/how-to-specify-binary-path-for-remote-chromedriver-in-codeception
# http://stackoverflow.com/questions/40262682/how-to-run-selenium-3-x-with-chrome-driver-through-terminal
# http://askubuntu.com/questions/760085/how-do-you-install-google-chrome-on-ubuntu-16-04

# Versions.
COLS="$(tput cols)"
CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`
SELENIUM_STANDALONE_VERSION=3.4.0
SELENIUM_SUBDIR=$(echo "$SELENIUM_STANDALONE_VERSION" | cut -d"." -f-2)

# Remove existing downloads and binaries so we can start from scratch.
SETUP="REMOVING EXISTING DOWNLOADS AND BINARIES"

printf "\n%."$COLS"d" 0 | sed s/0/+/g
printf "%."$[ ($COLS - ${#SETUP}) / 2 ]"d" 0 | sed s/0/" "/g
printf "$SETUP"
printf "\n%."$COLS"d" 0 | sed s/0/+/g

sudo apt-get remove google-chrome-stable
rm ~/selenium-server-standalone-*.jar
rm ~/chromedriver_linux64.zip
sudo rm /usr/local/bin/chromedriver
sudo rm /usr/local/bin/selenium-server-standalone.jar

# Install dependencies.
SETUP="INSTALLING DEPENDENCIES"

printf "\n%."$COLS"d" 0 | sed s/0/+/g
printf "%."$[ ($COLS - ${#SETUP}) / 2 ]"d" 0 | sed s/0/" "/g
printf "$SETUP"
printf "\n%."$COLS"d" 0 | sed s/0/+/g

sudo apt-get update
sudo apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4

# Install Chrome.
SETUP="INSTALLING CHROME"

printf "\n%."$COLS"d" 0 | sed s/0/+/g
printf "%."$[ ($COLS - ${#SETUP}) / 2 ]"d" 0 | sed s/0/" "/g
printf "$SETUP"
printf "\n%."$COLS"d" 0 | sed s/0/+/g

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install google-chrome-stable

# Install ChromeDriver.
SETUP="INSTALLING CHROMEDRIVER"

printf "\n%."$COLS"d" 0 | sed s/0/+/g
printf "%."$[ ($COLS - ${#SETUP}) / 2 ]"d" 0 | sed s/0/" "/g
printf "$SETUP"
printf "\n%."$COLS"d" 0 | sed s/0/+/g

wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
rm ~/chromedriver_linux64.zip
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver

# Install Selenium Server.
SETUP="INSTALLING SELENIUM SERVER"

printf "\n%."$COLS"d" 0 | sed s/0/+/g
printf "%."$[ ($COLS - ${#SETUP}) / 2 ]"d" 0 | sed s/0/" "/g
printf "$SETUP"
printf "\n%."$COLS"d" 0 | sed s/0/+/g

wget -N http://selenium-release.storage.googleapis.com/$SELENIUM_SUBDIR/selenium-server-standalone-$SELENIUM_STANDALONE_VERSION.jar -P ~/
sudo mv -f ~/selenium-server-standalone-$SELENIUM_STANDALONE_VERSION.jar /usr/local/bin/selenium-server-standalone.jar
sudo chown root:root /usr/local/bin/selenium-server-standalone.jar
sudo chmod 0755 /usr/local/bin/selenium-server-standalone.jar

# Install Python.
SETUP="INSTALLING PYTHON"

printf "\n%."$COLS"d" 0 | sed s/0/+/g
printf "%."$[ ($COLS - ${#SETUP}) / 2 ]"d" 0 | sed s/0/" "/g
printf "$SETUP"
printf "\n%."$COLS"d" 0 | sed s/0/+/g

sudo apt-get update
sudo apt-get -y upgrade
sudo apt autoremove
sudo apt-get install python3
sudo apt-get install python3-pip

# Install Selenium and Requests modules.
SETUP="INSTALLING MODULES"

printf "\n%."$COLS"d" 0 | sed s/0/+/g
printf "%."$[ ($COLS - ${#SETUP}) / 2 ]"d" 0 | sed s/0/" "/g
printf "$SETUP"
printf "\n%."$COLS"d" 0 | sed s/0/+/g

sudo pip3 install --upgrade pip
sudo pip3 install selenium
sudo pip3 install requests

# Instalation finished.
SETUP="INSTALLATION FINISHED"

printf "\n%."$COLS"d" 0 | sed s/0/+/g
printf "%."$[ ($COLS - ${#SETUP}) / 2 ]"d" 0 | sed s/0/" "/g
printf "$SETUP"
printf "\n%."$COLS"d" 0 | sed s/0/+/g

