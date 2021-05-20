#!/usr/bin/env python3

# Definitely gonna put some tests in here
from selenium import webdriver
import time

login_url = "https://users.nexusmods.com/auth/sign_in"
mod_url = "https://www.nexusmods.com/morrowind/mods/19510?tab=files&file_id=1000007846"

# Set and ask for WebDriver
# FF WebDriver https://github.com/mozilla/geckodriver/releases
# Chrome WebDriver https://sites.google.com/a/chromium.org/chromedriver/downloads

# Logging into nexusmods.com

def site_login(login_url, username, password):
    driver.get(login_url)
    driver.find_element_by_id("user_login").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_name("commit").click()

username = input("NexusMods username?: ")
password = input("NexusMods password?: ")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'], "detach", True)
driver = webdriver.Chrome(options=options)

site_login(login_url, username, password)

# Downloading mods

def mod_dl(mod_url):
    driver.get(mod_url)
    slow_dl_button = driver.find_elements_by_xpath("//button[@id='slowDownloadButton']")[0]
    slow_dl_button.click()

mod_dl(mod_url)