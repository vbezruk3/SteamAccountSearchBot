import time

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

import re

from bs4 import BeautifulSoup

import requests

from webdriver_manager.chrome import ChromeDriverManager

from bot.config import *

import bot.chains.func.files as files

countries = []

def init():
    global driver, countries

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    countries = files.loadFile(countries_dir)

async def getId(url):
    url = f'{url}/?xml=1'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="html.parser")

    tables = str(soup.find_all('steamid64'))[12:].replace('</steamid64>]', '')

    return tables

async def getInf(id):
    url = f'https://steamid.pro/lookup/{id}'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="html.parser")

    tables = str(soup.find_all('ul', {'class': 'player-info'}))

    lk = tables.find('Level <span>')
    k = 0

    level = ''

    print(tables[lk:(lk+30)])

    while tables[lk + 12 + k] != '<':
        level += tables[lk + 12 + k]

        k += 1

        if k > 3:
            level = 'none'

            break

    rk = tables.find('"number" title="">')
    k = 0

    rank = ''

    while tables[rk + 18 + k] != 'y' and tables[rk + 18 + k] != 'm':
        rank += tables[rk + 18 + k]

        k += 1

        if k > 3:
            rank = 'none'

            break

    ck = tables.find('flag-icon-') + 10

    k = 0

    country = ''

    while tables[ck + k] != '"':
        country += tables[ck + k]

        k += 1

    if country not in countries:
        country = 'none'

    return [level, rank, country]

async def getCost(url):

    '''
    url = f'https://csgobackpack.net/index.php?nick={id}'

    driver.get(url)

    time.sleep(1)

    text = str(driver.page_source)

    if 'In total' in text:

        ans = text.find('In total') + 11

        cost = ''

        dollar = 1.18116

        while text[ans] != ' ':
            ans += 1

            cost += text[ans]

        if '€' in cost:
            cost = float(cost.replace('€', '')) * dollar
        else:
            cost = float(cost.replace('$', ''))

        return cost
    else:
        return 'none'
    '''

    url = f'{url}/inventory/#730'

    driver.get(url)

    time.sleep(sleep_time1)

    try:
        element = driver.find_element_by_class_name("error_ctn")

        return 'error'
    except:
        pass

    try:
        element = driver.find_element_by_class_name("load_error_icon")

        return 'error_load'
    except:
        pass

    try:
        element = driver.find_element_by_id("invValue")
    except:
        return 'none'

    tables = 'агрузка...'

    k = 0

    while tables == 'агрузка...':

        if k > 3:
            return 'none'

        k += 1

        element.click()

        time.sleep(sleep_time2)

        soup = BeautifulSoup(driver.page_source, features="html.parser")
        tables = str(soup.find_all('span', {'class': 'priceValue'})[0])[26:].replace('</span>', '')

        tables = tables.replace(',', '')

        time.sleep(0.5)

    tables = float(tables)

    return tables

async def getAll(url):
    cost = await getCost(url)
    id = await getId(url)
    #cost = await getCost(id)
    inf = await getInf(id)

    inf.append(cost)

    return inf