import manager as manager
import requests
from bs4 import BeautifulSoup
import pandas as pd

import re

import json

from bs4 import BeautifulSoup
import urlopen

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def getId(url):
    url = f'https://steamid.xyz/{url}'

    htmlContent = requests.get(url, verify=False)

    # htmlContent.content
    soup = BeautifulSoup(htmlContent.text, features="html.parser")

    data=str(soup.find_all('input', {'onclick': 'this.select();'}))

    data=re.findall(r'value="\d+', data)

    data = data[1].replace('value="', '')

    print(data)

    # soup = BeautifulSoup(data)

    #print(data)


def getCost(id):

    url = f'http://csgobackpack.net/api/GetInventoryValue/?id={id}'
    htmlContent = requests.get(url, verify=False)

   # htmlContent.content
    data = htmlContent.json()

   # soup = BeautifulSoup(data)

    print(data['value'])

    return




