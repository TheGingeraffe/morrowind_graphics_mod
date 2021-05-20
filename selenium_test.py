#!/usr/bin/env python3

# Definitely gonna put some tests in here
from selenium import webdriver
import time

mod_url = "https://www.nexusmods.com/morrowind/mods/19510?tab=files&file_id=1000007846"

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location = "C:\Drivers\chromedriver.exe"
#options.binary_location = "/usr/bin/chromium"
driver = webdriver.Chrome(chrome_options=options)
driver.get(mod_url)

# click Slow Download
slow_dl_button = driver.find_elements_by_xpath("//button[@id='slowDownloadButton']")[0]
slow_dl_button.click()
