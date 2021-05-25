#!/usr/bin/env python3

# Packages
import platform
import sys
import shutil
import os
import datetime
import winreg
from selenium import webdriver
import time

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
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
        morrowind_path = (steam_path[0] + "\steamapps\common\Morrowind")
        print("Morrowind install located at " + morrowind_path)
    elif operating_system == "Linux":
        print("You are using Linux")
        exit
    elif operating_system == "Darwin":
        print("You are using MacOS")
        exit
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

# Downloads mods

login_url = "https://users.nexusmods.com/auth/sign_in"

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
# chrome_options.add_argument("--headless")
prefs = {"download.default_directory" : mod_path}
chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(options=chrome_options)

# This pop-up breaks it https://www.nexusmods.com/morrowind/mods/41102

def mod_dl(mod_url):
    driver.get(mod_url)
    if "nexusmods" in mod_url:
        manual_download_section = driver.find_element_by_id("action-manual")
        download_button = manual_download_section.find_element_by_tag_name('a')
        download_link = (download_button.get_attribute('href'))
        driver.get(download_link)
        time.sleep(2)
        #  If file_id doesn't exist, there is more than one main file
        file_id = download_link.split("file_id=")
        time.sleep(2)
        if len(file_id) > 1:
            driver.get("https://www.nexusmods.com/Core/Libs/Common/Widgets/DownloadPopUp?id=" + file_id[1] + "&game_id=100&source=FileExpander")
        else:
            driver.get(download_link)
            mod_files = driver.find_element_by_id("mod_files")
            download_button = mod_files.find_element_by_xpath("//span[text()='Manual download']")
            download_button.click()
            if "ModRequirementsPopUp" in driver.current_url:
                file_id = driver.current_url.split("id=")
                file_id = file_id[1].split('&')
                driver.get("https://www.nexusmods.com/Core/Libs/Common/Widgets/DownloadPopUp?id=" + file_id[0] + "&game_id=100&source=FileExpander")
            file_id = driver.current_url.split("file_id=")
            driver.get("https://www.nexusmods.com/Core/Libs/Common/Widgets/DownloadPopUp?id=" + file_id[1] + "&game_id=100&source=FileExpander")
 
    elif "modhistory" in mod_url:
        download_button = driver.find_element_by_id("dlb")
        download_button.click()

site_login(login_url, username, password)

# Downloading from modhistory.com and other misc sources

with open('modlist.txt') as modlist:
    for mod in modlist:
        mod_dl(mod)

# Installs mods

