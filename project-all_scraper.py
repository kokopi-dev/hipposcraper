#!/usr/bin/env python2
"""Creates directory and files for Holberton School projects.

Usage: `./project-all_scraper.py project_link`

Scrapes information to create the directory, task files,
test files, and header for a given project.

Displays error messages for any failed scrapes.
"""
import os
import sys
import re
import string
import json
import urllib2
import cookielib
import mechanize
from bs4 import BeautifulSoup
from scrapers import *

# Program variables
current_path = os.path.dirname(os.path.abspath(__file__))
valid_link = 'intranet.hbtn.io/projects'
valid_header = '.h'

# Command Line Arguments
arg = sys.argv[1:]
count = len(arg)

# Argument Checker
if count > 1:
    print("[ERROR] Too many arguments (must be one)")
    sys.exit()
elif count == 0:
    print("[ERROR] Too few arguments (must be one)")
    sys.exit()

link = sys.argv[1]
while not (valid_link in link):
    print("[ERROR] Invalid link (must be to project on intranet.hbtn.io)")
    link = raw_input("Enter link to project: ")

print("Creating project:")

# Intranet login credentials
with open(("%s/auth_data.json" % current_path), "r") as my_keys:
    intra_keys = json.load(my_keys)

# Login Variable
login = "https://intranet.hbtn.io/auth/sign_in"

# Logging into website
cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open(login)

sys.stdout.write("  -> Logging in... ")
try:
    br.select_form(nr=0)
    br.form['user[login]'] = intra_keys["intra_user_key"]
    br.form['user[password]'] = intra_keys["intra_pass_key"]
    br.submit()
    my_keys.close()

    # Parsing page into html soup
    page = br.open(link)
    soup = BeautifulSoup(page, 'html.parser')

    # --- Checking if it is a C or Python project ---
    find_project_type = soup.find(string=re.compile("GitHub repository: "))
    find_project_type = find_project_type.next_sibling.text

    # Finding directory
    find_dir = soup.find(string=re.compile("Directory: "))
    dir_name = find_dir.next_element.text

    print("done")
except AttributeError:
    print("[ERROR] Login failed - are your auth_data credentials correct?")
    sys.exit()

# --- Python Project Scraper ---
if "higher_level" in find_project_type:
    # Making and changing to proper directory
    sys.stdout.write("  -> Creating directory... ")
    try:
        os.mkdir(dir_name)
        os.chdir(dir_name)
        print("done")
    except OSError:
        print("[ERROR] Failed to create directory - does it already exist?")
        sys.exit()

    # Creating file(s) from scrapers.py_scraper
    sys.stdout.write("  -> Creating task files... ")
    find_file_name = soup.find_all(string=re.compile("File: "))
    py_proto_tag = soup.find_all(string=re.compile("Prototype: "))

    scrape_py(find_file_name, py_proto_tag)
    print("done")

    # Finding and making py main files
    sys.stdout.write("  -> Creating test files... ")
    find_pre = soup.select("pre")

    scrape_tests(find_pre)
    print("done")

    # Giving permissions to .py files
    sys.stdout.write("  -> Setting permissions... ")
    try:
        os.system("chmod u+x *.py")
        print("done")
    except OSError:
        print("[ERROR] Failed to set permissions.")

    print("Project all set!")

# --- C Project Scraper ---
elif "low_level" in find_project_type:
    # Making and changing to proper directory
    sys.stdout.write("  -> Creating directory... ")
    try:
        os.mkdir(dir_name)
        os.chdir(dir_name)
        print("done")
    except OSError:
        print("[Error] Failed to create directory - does it already exist?")
        sys.exit()

    # Setting _putchar variables and scraping it
    sys.stdout.write("  -> Checking for _putchar... ")
    find_putchar = soup.find(string=re.compile("You are allowed to use"))
    try:
        if len(find_putchar) == 23:
            scrape_putchar(find_putchar)
    except TypeError:
        pass

    # Setting header variable
    thereIsHeader = 0
    header_str = "forget to push your header file"
    try:
        find_header = soup.find(string=re.compile(header_str)).previous_element
    except AttributeError:
        thereIsHeader = 1

    # Make header file, if none, skip and make files
    if thereIsHeader == 0:
        # Variables for function name array
        proto_store = []
        get_header_name = find_header.previous_element.previous_element

        # Making prototype names array
        find_proto = soup.find_all(string=re.compile("Prototype: "))
        for li in find_proto:
            proto_store.append(li.next_sibling.text.replace(";", ""))

        # Making C files with function name array
        sys.stdout.write("  -> Creating task files... ")
        find_file_name = soup.find_all(string=re.compile("File: "))

        # Creating C files
        scrape_c(find_file_name, get_header_name, proto_store)
        print("done")

        # Find header prototype
        find_proto_h = soup.find_all(string=re.compile("Prototype: "))

        # Creating header file
        scrape_header(find_proto_h, get_header_name, find_putchar)
    else:
        # Making C files with function name array
        sys.stdout.write("  -> Creating task files... ")
        find_file_name = soup.find_all(string=re.compile("File: "))
        proto_store = 0
        get_header_name = 0
        scrape_c(find_file_name, get_header_name, proto_store)
        print("done")

    # Finding and making c main files
    sys.stdout.write("  -> Creating test files... ")
    find_pre = soup.select("pre")
    scrape_tests(find_pre)
    print("done")

    # Giving permissions to .c files
    sys.stdout.write("  -> Setting permissions... ")
    try:
        os.system("chmod u+x *.c")
        print("done")
    except OSError:
        print("[ERROR] Failed to set permissions")

    print("Project all set!")

# -- Bash Project Scraper--
elif "system" in find_project_type:
    # Making and changing to proper directory
    sys.stdout.write("  -> Creating directory... ")
    try:
        os.mkdir(dir_name)
        os.chdir(dir_name)
        print("done")
    except OSError:
        print("[ERROR] Failed to create directory - does it already exist?")
        sys.exit()

    # Creating file(s) from scrapers.py_scraper
    sys.stdout.write("  -> Creating task files... ")
    find_file_name = soup.find_all(string=re.compile("File: "))
    scrape_bash(find_file_name)
    print("done")

    # Giving permissions to all files
    sys.stdout.write("  -> Setting permissions... ")
    try:
        os.system("chmod u+x *")
        print("done")
    except OSError:
        print("[ERROR] Failed to set permissions")

    print("Project all set!")
else:
    print("[ERROR]: Could not determine project type")
    sys.exit(1)
