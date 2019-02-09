#!/usr/bin/env python2
"""Creates README.md files for Holberton School projects.

Usage: `./holberton-read_t.py project_link`

Scrapes project title as well as task filenames, descriptions, and
learning objectives. Creates the README.md in the corresponding project
directory if it already exists. Otherwise, creates the file in the
current directory.

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
from bs4 import BeautifulSoup, Comment

# Program variables
current_path = os.path.dirname(os.path.abspath(__file__))
valid_link = 'intranet.hbtn.io/projects'

# Command line arugments
arg = sys.argv[1:]
argcount = len(arg)

print("Creating README.md file:")
# Argument checker
if argcount > 1:
    print("[ERROR] Too many arguments (must be one)")
    sys.exit()
elif argcount == 0:
    print("[ERROR] Too few arguments (must be one)")
    sys.exit()

link = sys.argv[1]
while not (valid_link in link):
    print("[ERROR] Invalid link (must be to project on intranet.hbtn.io)")
    link = raw_input("Enter link to project: ")

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

br.select_form(nr=0)
br.form['user[login]'] = intra_keys["intra_user_key"]
br.form['user[password]'] = intra_keys["intra_pass_key"]
br.submit()

my_keys.close()

# Parsing page into html soup
page = br.open(link)
soup = BeautifulSoup(page, 'html.parser')

# ---------------------------------
# ----------- Scrapers ------------
# ---------------------------------
sys.stdout.write("  -> Scraping information... ")

# Finding project title
prj_title = soup.find("h1")

# Finding directory
find_dir = soup.find(string=re.compile("Directory: "))
dir_name = find_dir.next_element.text

# Scraping learning objectives
try:
    find_project_type = soup.find(string=re.compile("GitHub repository: "))
    find_project_type = find_project_type.next_sibling.text

    """
    # Python "what you should learn"
    if "higher_level" in find_project_type:
        string = "without the help of Google"
        prj_info = soup.find("strong", string=re.compile(string))
        prj_info_t = prj_info.next_element.next_element
        prj_info_t = prj_info_t.next_element.next_element.text.encode('utf-8')

    # C "what you should learn"
    elif "low_level" in find_project_type:
        string = "At the end of this project you are expected"
        prj_info = soup.find("p", string=re.compile(string))
        prj_info_t = prj_info.next_element.next_element
        prj_info_t = prj_info_t.next_element.text.encode('utf-8')

    # Bash "what you should learn"
    elif "system" in find_project_type:
        prj_info = soup.find("h3", string=re.compile("General"))
        prj_info_t = prj_info.next_element.next_element.next_element.text
    """
    prj_info = soup.find("h2", string=re.compile("Learning Objectives"))
    prj_info_t = prj_info.find_next("h3").next_element.next_element.next_element.text
    # Storing project info into an array
    prj_info_arr = prj_info_t.splitlines()

except AttributeError:
    print("[ERROR] Failed to scrape learning objectives")
    sys.stdout.write("                         ... ")
    prj_info_arr = None
    pass

try:
    # Scraping file names
    file_name = soup.find_all(string=re.compile("File: "))
    file_name_arr = []
    # Store file names into arr
    for idx in file_name:
        file_text = idx.next_sibling.text
        # Finding comma index for multiple files listed
        find_comma = file_text.find(",")
        if find_comma != -1:
            file_name_arr.append(file_text[:find_comma])
        else:
            file_name_arr.append(file_text)
except (IndexError, AttributeError):
    print("[ERROR] Failed to scrape file names")
    sys.stdout.write("                         ... ")
    file_name_arr = None
    pass

try:
    # Finding task titles
    my_tasks = soup.find_all("h4", class_="task")
    my_tasks_arr = []
    # Store task titles into arr
    for idx in my_tasks:
        item = idx.next_element.strip("\n").strip()
        my_tasks_arr.append(item)
except (IndexError, AttributeError):
    print("[ERROR] Failed to scrape task titles")
    sys.stdout.write("                         ... ")
    my_tasks_arr = None
    pass

try:
    # Finding task descriptions
    task_info = soup.find_all(string=lambda text: isinstance(text, Comment))
    task_info_arr = []
    # Store task info into arr
    for comments in task_info:
        if comments == " Task Body ":
            info_text = comments.next_element.next_element.text
            task_info_arr.append(info_text.encode('utf-8'))
except (IndexError, AttributeError):
    print("[ERROR] Failed to scrape task descriptions")
    print("                         ... ")
    task_info_arr = None
    pass

print("done")

# ---------------- Extra Scrapes ------------------
# --- Remove comments to use the list variables ---
# -------------------------------------------------
"""
# Finding requirements based on project type
req_str = "Requirements"
req_arr = []
if find_project_type == "holbertonschool-higher_level_programming":
    req_str = "Requirements for Python scripts"

req_tag = soup.find("h2", string=re.compile(req_str))
req = req_tag.next_element.next_element.next_element
# Store requirements info into arr
for li in req:
    try:
        req_arr.append(li.text)
    except AttributeError:
        pass
"""

# -----------------------------------------
# ---------- README TEMPLATE BELOW --------
# --- Modify to write your own template ---
# -----------------------------------------

try:
    filename = dir_name + "/README.md"
    rtemp = open(filename, "w+")
except IOError:
    rtemp = open("README.md", "w")

sys.stdout.write("  -> Writing project title... ")
rtemp.write("# %s\n" % prj_title.text)
rtemp.write("\n")
print("done")

if prj_info_arr is not None:
    sys.stdout.write("  -> Writing learning objectives... ")
    rtemp.write("## Description\n")
    rtemp.write("What you should learn from this project:\n")

    try:
        for item in prj_info_arr:
            if len(item) == 0:
                rtemp.write("{}\n".format(item))
                continue
            rtemp.write("* {}\n".format(item))
        print("done")
    except (AttributeError, IndexError, UnicodeEncodeError):
        print("[ERROR] Failed to write learning objectives.")
        pass

rtemp.write("\n")
rtemp.write("---\n")

if (my_tasks_arr is not None and
        file_name_arr is not None and
        task_info_arr is not None):
    sys.stdout.write("  -> Writing task information... ")
    count = 0
    while count < len(my_tasks_arr):
        try:
            rtemp.write("\n")
            rtemp.write("### [%s](./%s)\n" % (my_tasks_arr[count],
                                              file_name_arr[count]))
            rtemp.write("* %s\n" % task_info_arr[count])
            rtemp.write("\n")
            count += 1
        except IndexError:
            print("Error: Could not write task %s" % file_name_arr[count])
            print("                                ... ")
            continue
    print("done")

sys.stdout.write("  -> Writing author information... ")
rtemp.write("---\n")
rtemp.write("\n")
rtemp.write("## Author\n")
rtemp.write("* **%s** - " % intra_keys["author_name"])
rtemp.write("[%s]" % intra_keys["github_username"])
rtemp.write("(%s)" % intra_keys["github_profile_link"])
print("done")

rtemp.close()

print("README.md all set!")
