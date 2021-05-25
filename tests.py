#!/usr/bin/env python3

# Definitely gonna put some tests in here

## Test requests to nexusmods with this format
## https://www.nexusmods.com/Core/Libs/Common/Widgets/DownloadPopUp?id=1000016238&game_id=100&source=FileExpander 



## https://www.nexusmods.com/Core/Libs/Common/Widgets/DownloadPopUp?id=${this can be found by inspecting element on the file on downloads page}&game_id=100&source=FileExpander

## Find file ids this way https://www.nexusmods.com/morrowind/mods/19510?tab=files&file_id=1000007846

from selenium import webdriver
import time

file_ids = []

login_url = "https://users.nexusmods.com/auth/sign_in"
mod_url = "https://www.nexusmods.com/morrowind/mods/19510?tab=files"
mod_path = "C:\Program Files (x86)\Steam\steamapps\common\Morrowind"

# TODO Set and ask for WebDriver
# Maybe try dockerized version with remote WebDriver?
# FF WebDriver https://github.com/mozilla/geckodriver/releases
# Chrome WebDriver https://sites.google.com/a/chromium.org/chromedriver/downloads

# Logging into nexusmods.com

def site_login(login_url, username, password):
    driver.get(login_url)
    driver.find_element_by_id("user_login").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_name("commit").click() 
    time.sleep(5)
    driver.find_element_by_partial_link_text("Nexus Mods Home").click()
    time.sleep(5)

username = input("NexusMods username?: ")
password = input("NexusMods password?: ")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
prefs = {"download.default_directory" : mod_path}
chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(options=chrome_options)

def mod_dl(mod_url):
    driver.get(mod_url)
    main_files = driver.find_element_by_id("file-container-main-files")
    main_file = main_files.find_element_by_class("file-expander-header clearfix accopen")
    print(main_file.get_attribute("data-id"))
site_login(login_url, username, password)
mod_dl(mod_url)
