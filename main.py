#!/usr/bin/env python3

# Packages
import getpass
import sys
import winreg

# Variables

username = getpass.getuser()

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
# Asks if Steam install

steam_installed = yesno("Is Morrowind installed with Steam?")

if steam_installed == True:
    if operating_system == "Windows":
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
        print(steam_path[0])
    elif operating_system == "Linux":
    elif operating_system == "Darwin":

# C:\Program Files (x86)\Steam\steamapps\common


# Else asks for Morrowind path

# Backs up install

# Downloads mods

# Installs mods