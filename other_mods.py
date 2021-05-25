#!/usr/bin/env python3

# Definitely gonna put some tests in here

from selenium import webdriver
import time

mod_path = "C:\Program Files (x86)\Steam\steamapps\common\Morrowind"

# TODO Set and ask for WebDriver
# Maybe try dockerized version with remote WebDriver?
# FF WebDriver https://github.com/mozilla/geckodriver/releases
# Chrome WebDriver https://sites.google.com/a/chromium.org/chromedriver/downloads

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
prefs = {"download.default_directory" : mod_path}
chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(options=chrome_options)

# modhistory downloads

def mod_dl(mod_url):
    driver.get(mod_url)
    download_button = driver.find_element_by_id("dlb")
    download_button.click()


with open('modhistory.txt') as modhistory:
    for mod in modhistory:
        mod_dl(mod)
