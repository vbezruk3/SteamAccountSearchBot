import os

from selenium import webdriver

TELEGRAM_BOT_TOKEN = '1867495675:AAFEUY4sqCdfbv-2OSm0pMA-TFW9C9ULlxI'

ADMIN_ID = '671836800'

extension_dir = './../extensions/Steam-Inventory-Helper.crx'

countries_dir = './../data/countries.json'

options = webdriver.ChromeOptions()

prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

options.add_extension(extension_dir)
options.add_argument("disable-popup-blocking")
options.add_argument("disable-infobars")

sleep_time1 = 1
sleep_time2 = 3

