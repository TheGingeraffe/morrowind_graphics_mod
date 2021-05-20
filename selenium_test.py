#!/usr/bin/env python3

# Definitely gonna put some tests in here
from selenium import webdriver
import time

mod_url = "https://www.nexusmods.com/morrowind/mods/19510?tab=files&file_id=1000007846"

# FF WebDriver https://github.com/mozilla/geckodriver/releases
# Chrome WebDriver https://sites.google.com/a/chromium.org/chromedriver/downloads

browser = webdriver.Chrome()
browser.get(mod_url)

# click Slow Download
slow_dl_button = browser.find_elements_by_xpath("//button[@id='slowDownloadButton']")[0]
slow_dl_button.click()
