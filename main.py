#!/usr/bin/env python3

# Packages
import platform
import sys
import shutil
import os
import datetime
import requests
from bs4 import BeautifulSoup

# Functions

def yesno(question):
    """Simple Yes/No Function."""
    prompt = f'{question} ? (y/n): '
    ans = input(prompt).strip().lower()
    if ans not in ['y', 'n']:
        print(f'{ans} is invalid, please try again...')
        return yesno(question)
    if ans == 'y':
        return True
    return False

# Returns Windows, Linux, or Darwin
operating_system = platform.system()

# Locates Morrowind install
steam_installed = yesno("Is Morrowind installed with Steam?")

if steam_installed == True:
    if operating_system == "Windows":
        import winreg
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
        morrowind_path = (steam_path[0] + "\steamapps\common\Morrowind")
        print("Morrowind install located at " + morrowind_path)
    elif operating_system == "Linux":
        print("You are using Linux")
    elif operating_system == "Darwin":
        print("You are using MacOS")
    else:
        morrowind_path = input("What is the full installation path of Morrowind? ")

# Backs up install
morrowind_backup = yesno("Back up your Morrowind installation? ")

if morrowind_backup == True:
    print("Backing up Morrowind installation... ")
    date_now = datetime.datetime.now()
    backup_destination = morrowind_path + date_now.strftime(".%m%d%Y_%H%M%S")
    copy_morrowind = shutil.copytree(morrowind_path, backup_destination)
    print("Morrowind backup location: ", copy_morrowind)


# Creates mod folder if doesn't exist

mod_path = os.path.join(morrowind_path, "mods")

if os.path.exists(mod_path) == False:
    os.mkdir(mod_path)
    print("Mod directory " + mod_path + " was created. ")
else:
    print("Mod directory " + mod_path + " already exists! ")

# Creates modlist

modlist_url = 'https://wiki.nexusmods.com/index.php/Morrowind_graphics_guide'
reqs = requests.get(modlist_url)
soup = BeautifulSoup(reqs.text, 'html.parser')

mod_urls = []
for link in soup.find_all("div", {"class": "mw-collapsible-content"}):
    mod_urls.append(link.find('a')['href'])

# Downloads mods

for mod_url in mod_urls:
    # If nexusmods URL, download one way
    print(mod_url)
    # If not, download another way

from selenium import webdriver
import time

file_ids = []

login_url = "https://users.nexusmods.com/auth/sign_in"
mod_url = "https://www.nexusmods.com/morrowind/mods/19510"
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
    time.sleep(2)
    driver.find_element_by_partial_link_text("Nexus Mods Home").click()
    time.sleep(2)

username = input("NexusMods username?: ")
password = input("NexusMods password?: ")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
prefs = {"download.default_directory" : mod_path}
chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(options=chrome_options)

def mod_dl(mod_url):
    driver.get(mod_url)
    if "nexusmods" in mod_url:
        manual_download_section = driver.find_element_by_id("action-manual")
        download_button = manual_download_section.find_element_by_tag_name('a')
        download_link = (download_button.get_attribute('href'))
        driver.get(download_link)
        slow_dl_button = driver.find_elements_by_xpath("//button[@id='slowDownloadButton']")[0]
        slow_dl_button.click()
    elif "modhistory" in mod_url:
        download_button = driver.find_element_by_id("dlb")
        download_button.click()

site_login(login_url, username, password)
mod_dl(mod_url)

# Downloading from modhistory.com and other misc sources

with open('miscmods.txt') as misc_mods:
    for mod in misc_mods:
        mod_dl(mod)

# Installs mods

