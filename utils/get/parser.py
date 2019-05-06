# Copyright (c) 2018-2019 Mx (Shift Project delegate / 4446910057799968777S)
# Licensed under MIT License <see LICENSE file>

import time

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from data import config

options = ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')

windows = config.os_windows


def DelegatesRedAndOrange(url, max_attempts, options=options):
    """
    Getts a data from Explorer's Delegate Monitor page.
    Using Selenium Web Browser Automation tool.
    This function starts a Chrome browser in headless mode.
    Then waits until delegates_table table loaded,
    then it checks is there any 'Missed block' or 'Not forging' delegates,
    if not, functions stops.
    If delegates table has one or more delegates with statuses
    'Not forging' anf 'Missed block' function saves data only with
    delegates with those statuses.

    Example of output:

    {
        1: {
            'NextTurn': '41 min 33 sec',
            'lastBlockTime': '2 days ago',
            'Name': 'kidnapped',
            'Status': 'Not forging'
        },
        5: {
            'NextTurn': '27 sec',
            'lastBlockTime': 'an hour ago',
            'Name': 'lol',
            'Status': 'Missed block'
        }
    }

    This function don't work with Firefox browser, because
    in gecodriver an action 'move_to_element' don't scroll the page.
    """

    # Please be sure you haven't slash ('/') at the end of an explorer link,
    # because in this case a Delegate Monitor tool page can't load a data.
    # I guess, it's kind of a bug.

    if url[-1] == '/':
        url = url[:-1]

    url += '/delegateMonitor'

    delegates_table = {}
    delegates_active = {}
    attempt = 0

    for i in range(max_attempts):
        try:
            if windows:
                # For Windows
                driver = webdriver.Chrome(chrome_options=options)
            else:
                # For Linux
                driver = webdriver.Chrome(
                    chrome_options=options,
                    executable_path=r'/usr/local/bin/chromedriver'
                )

            actions = ActionChains(driver)
            driver.get(url)
            wait = WebDriverWait(driver, 10)

            green_circle = 'i.green'
            red_circle = 'i.red'
            orange_circle = 'i.orange'

            # Waiting until a delegates table will be definitely loaded
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, green_circle))
            )
            """
            Waiting for explorer to be shure there all is okay
            Sometimes explorer shows delegates_table as "Missed block"
            or "Not forging" after fast loading while it's not.
            """
            time.sleep(3)

            if attempt > 2:
                time.sleep(17)

            for i in range(1, 102):
                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[2]/a'
                    .format(i)
                ).get_attribute("innerHTML")
                delegates_active[i] = str(elem)

                actions.reset_actions()

            missed_block_total_elem = driver.find_element_by_xpath(
                '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]/div'
                '/div/div/div[1]/div[1]/div[2]/div/p'
            ).get_attribute("innerHTML")

            not_forging_total_elem = driver.find_element_by_xpath(
                '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]/div'
                '/div/div/div[1]/div[1]/div[3]/div/p'
            ).get_attribute("innerHTML")

            zero_missed_block = int(missed_block_total_elem) == 0
            zero_not_forging = int(not_forging_total_elem) == 0

            if zero_missed_block and zero_not_forging:
                break

            circles_orange = (
                driver.find_elements_by_css_selector(orange_circle)
            )
            circles_red = (
                driver.find_elements_by_css_selector(red_circle)
            )

            def RankFromCircle(circles):
                rank = []

                for i in circles:
                    table_row = (
                        i
                        .find_element_by_xpath('..')
                        .find_element_by_xpath('..')
                    )
                    rank_elem = table_row.find_element_by_css_selector(
                        'td:nth-child(1)'
                    ).get_attribute("innerHTML")
                    rank.append(int(rank_elem))

                return rank

            red_and_orange = (
                RankFromCircle(circles_orange) + RankFromCircle(circles_red)
            )

            for i in red_and_orange:
                delegates_table[i] = {}
                delegates_table[i]['Name'] = 'Name'
                delegates_table[i]['Status'] = 'Missed block'
                delegates_table[i]['NextTurn'] = '45 min'
                # Trying to avoid error:
                # Message: no such element: Unable to locate element
                delegates_table[i]['lastBlockTime'] = '∞ ago'

                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[2]/a'
                    .format(i)
                ).get_attribute("innerHTML")
                delegates_table[i]['Name'] = str(elem)

                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[5]'
                    .format(i)
                ).get_attribute("innerHTML")
                delegates_table[i]['NextTurn'] = str(elem)

                elem = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]/td[6]/i'
                    .format(i)
                ).get_attribute("outerHTML")

                not_forging = 'red' in str(elem)
                missed_block = 'orange' in str(elem)

                if not_forging:
                    delegates_table[i]['Status'] = 'Not forging'

                if missed_block:
                    delegates_table[i]['Status'] = 'Missed block'

                # Hovering over a circle to get status info visible
                element_to_hover_over = driver.find_element_by_xpath(
                    '//*[@id="wrap"]/section/div/delegate-monitor/div/div[5]'
                    '/div/div/div/div[1]/div[3]/table/tbody[2]/tr[{0}]'
                    '/td[6]/i'.format(i)
                )
                actions.move_to_element(element_to_hover_over).perform()
                # Trying to avoid error:
                # 'Message: no such element: Unable to locate element:'
                time.sleep(1)
                try:
                    elem = driver.find_element_by_xpath(
                        '//*[@id="wrap"]/section/div/'
                        'delegate-monitor/div/div[5]'
                        '/div/div/div/div[1]/div[3]/'
                        'table/tbody[2]/tr[{0}]/td[6]'
                        '/div/div[2]'.format(i)
                    ).get_attribute("innerHTML")
                    delegates_table[i]['lastBlockTime'] = (
                        str(elem).split('<br>')[2]
                    )
                except:
                    delegates_table[i]['lastBlockTime'] = 'undefined'

                actions.reset_actions()
            break
        except Exception as ex:
            print('Error #{num}:'.format(num=attempt))
            print(ex)
            # Catching exeption when driver is not assigned
            try:
                driver.quit()
            except:
                pass
            attempt += 1
            pass
        finally:
            # Catching exeption when driver is not assigned
            try:
                driver.quit()
            except:
                pass

    return delegates_table, delegates_active, attempt


# Checking explorers` online
# explorer_online = check.isOnline(url, 3, 5)
# explorer_mirror_online = check.isOnline(url_mirror, 3, 5)

# if 'explorers' not in last_msg:
#     last_msg['explorers'] = {}
#     last_msg['explorers']['online'] = True

# if double_checking and (not explorer_online or not explorer_mirror_online):

#     last_msg, delay = check.explorersTimeout(last_msg)
#     last_msg['explorers']['online'] = False

#     if not delay:
#         send.explorersBadMessage(
#             last_msg, url, url_mirror, explorer_online,
#             explorer_mirror_online
#         )

#     message_explorers = send.formingExplorersMessage(
#         url, url_mirror, explorer_online, explorer_mirror_online,
#         'telegram',
#     )
#     send.TelegramDebug(message_explorers, 'Explorers')

#     # Saving data to a file
#     with open(LAST_MSG_PATH, mode='w', encoding='utf-8') as f:
#         json.dump(last_msg, f)

#     # Exit from the script
#     raise SystemExit

# # Sending a good message if both explorers is online now
# if not last_msg['explorers']['online']:
#     last_msg = send.explorersGoodMessage(
#             last_msg, url, url_mirror, explorer_online,
#             explorer_mirror_online
#         )
