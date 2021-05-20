#!/usr/bin/env python3

# Packages
import platform
import sys
import shutil
import os
import datetime
import requests
from bs4 import BeautifulSoup

# Variables

# Returns Windows, Linux, or Darwin
operating_system = platform.system()

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


# Locates Morrowind install
steam_installed = yesno("Is Morrowind installed with Steam?")

if steam_installed == True:
    if operating_system == "Windows":
        import winreg
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                              "SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
        morrowind_path = (steam_path[0] + "\steamapps\common\Morrowind")
        print("Morrowind install located at " + morrowind_path)
        elif operating_system == "Linux":
            print("You are using Linux")
        elif operating_system == "Darwin":
            print("You are using MacOS")
    else:
        morrowind_path = input(
            "What is the full installation path of Morrowind? ")

# Backs up install
morrowind_backup = yesno("Back up your Morrowind installation? ")

if morrowind_backup == True:
    print("Backing up Morrowind installation... ")
    date_now = datetime.datetime.now()
    backup_destination = morrowind_path + \
        date_now.strftime(".%m%d%Y_%H%M%S")
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

# Installs mods
