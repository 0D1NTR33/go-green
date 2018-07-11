# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')


def Delegates(url, max_attempts, options=options):
    """
    Getting a data from Explorer's Delegate Monitor page.
    Using Selenium Web Browser Automation tool.
    This function starts a Chrome browser in headless mode.
    Then waits until delegates table loaded,
    then it saves data from each delegates row.
    Such data as 'Name', 'ForgingTime', metadata from 'Circle'
    and time of the last forged block from 'Status' column.
    This function don't work with Firefox browser, because
    in gecodriver an action 'move_to_element' don't scroll the page.

    """

    delegates = {}
    attempt = 0

    for i in range(max_attempts):
        try:
            # driver = webdriver.Chrome(chrome_options=options)
            driver = webdriver.Chrome(
                chrome_options=options,
                executable_path=r'/usr/local/bin/chromedriver'
            )
            actions = ActionChains(driver)
            driver.get(url)
            wait = WebDriverWait(driver, 10)

            """
            Trying to open Delegate Monitor from main page.
            But it's not working. Selenium can't click to
            dropdown menu selector.
            """
            # Opening an explorer's main page
            # wait.until(
            #     EC.presence_of_element_located((
            #         By.CSS_SELECTOR, "a.tools-menu"
            #     ))
            # )
            # Clicking to a "Tools" dropdown menu
            # element_to_click = driver.find_element_by_xpath(
            #     '//*[@id="main-menu-dropdown"]'
            # )
            # actions.click(element_to_click).pause(5).perform()

            # # Clicking to "Delegate monitor" link
            # element_to_click = driver.find_element_by_xpath(
            #     '//*[@id="header"]/div[2]/ul/li[2]/ul/li[3]'
            # )
            # actions.move_to_element(element_to_click).click().perform()

            # Waiting until a delegates table will be definitely loaded
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "i.red"))
            )

            i = 1
            while i <= 101:
                delegates[i] = {}

                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[2]/a'
                    .format(i)
                ).get_attribute("innerHTML")
                delegates[i]['Name'] = str(elem)

                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[5]'
                    .format(i)
                ).get_attribute("innerHTML")
                delegates[i]['ForgingTime'] = str(elem)

                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[6]/i'
                    .format(i)
                ).get_attribute("outerHTML")
                delegates[i]['Circle'] = str(elem)

                # Hovering over a circle to get status info visible
                element_to_hover_over = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]'
                    '/td[6]/i'.format(i)
                )
                actions.move_to_element(element_to_hover_over).perform()
                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[6]'
                    '/div/div[2]'.format(i)
                ).get_attribute("innerHTML")
                delegates[i]['lastBlockTime'] = str(elem).split('<br>')[2]

                actions.reset_actions()
                i += 1
            break
        except Exception as ex:
            print('Error #{num}:'.format(num=attempt))
            print(ex)
            try:
                driver.quit()
            except:
                pass
            attempt += 1
            # time.sleep(215) # ~100 times per 6 hours
            pass
        finally:
            try:
                driver.quit()
            except:
                pass
    return delegates
