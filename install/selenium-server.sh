#!/usr/bin/env bash

# Run Chrome via Selenium Server
start-chrome() {
    xvfb-run java -Dwebdriver.chrome.driver=/usr/local/bin/chromedriver -jar /usr/local/bin/selenium-server-standalone.jar
}

start-chrome-debug() {
    xvfb-run java -Dwebdriver.chrome.driver=/usr/local/bin/chromedriver -jar /usr/local/bin/selenium-server-standalone.jar -debug
}

# Run Chrome Headless
start-chrome-headless() {
    chromedriver --url-base=/wd/hub
}

#Run Test
test-path() {
    OK=true

    if test -f "/usr/local/bin/chromedriver";
    then
        echo "chromedriver: Ok!"
    else
        echo "File "chromedriver" not exists or not in path"
        OK=false
    fi

    if test -f "/usr/local/bin/selenium-server-standalone.jar";
    then
        echo "selenium-server: Ok!"
    else
        echo "File "selenium-server" not exists or not in path"
        OK=false
    fi

    if [ "$OK" == false ]
    then
        echo "Test not passed!"
    else
        echo "Test passed."
    fi
}

"$@"
# Run
# start-chrome
# start-chrome-debug
# start-chrome-headless
# test-path