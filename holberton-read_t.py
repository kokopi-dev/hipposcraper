#!/usr/bin/python2
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

# Argument checker
if argcount > 1:
    print("  <Error: Too many arguments (must be one)>")
    sys.exit()
elif argcount == 0:
    print("  <Error: Too few arguments (must be one)>")
    sys.exit()

link = sys.argv[1]
while not (valid_link in link):
    print("  <Error: Invalid link (must be to project on intranet.hbtn.io)>")
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

# Finding project title
prj_title = soup.find("h1")

# Checking for C or Python project page
find_project_type = soup.find(string=re.compile("GitHub repository: ")).next_sibling.text

# Python "what you should learn"
if "higher_level" in find_project_type:
    prj_info = soup.find("strong", string=re.compile("without the help of Google"))
    prj_info_t = prj_info.next_element.next_element.next_element.next_element.text.encode('utf-8')
 
# C "what you should learn"
elif "low_level" in find_project_type:
    prj_info = soup.find("p", string=re.compile("At the end of this project you are expected"))
    prj_info_t = prj_info.next_element.next_element.next_element.text.encode('utf-8')

# Bash "what you should learn"
elif "system" in find_project_type:
    prj_info = soup.find("h3", string=re.compile("General"))
    prj_info_t = prj_info.next_element.next_element.next_element.text 

else:
    print("Fatal Error: Could not find project's type\n")
    exit(1)

# ---------------------------------
# ----------- Scrapers ------------
# ---------------------------------

# Storing project info into an array
prj_info_arr = prj_info_t.splitlines()

# Finding file names
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

# Finding task titles
my_tasks = soup.find_all("h4", class_="task")
my_tasks_arr = []
# Store task titles into arr
for idx in my_tasks:
    item = idx.next_element.strip("\n").strip()
    my_tasks_arr.append(item)

# Finding task descriptions
task_info = soup.find_all(string=lambda text:isinstance(text, Comment))
task_info_arr = []
# Store task info into arr
for comments in task_info:
    if comments == " Task Body ":
        task_info_arr.append(comments.next_element.next_element.text.encode('utf-8'))

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

print("Creating README.md... ")
with open(("%s/auth_data.json" % current_path), "r") as my_keys:
	github_keys = json.load(my_keys)
rtemp = open("temp_README", "w+")

rtemp.write("# %s\n" % prj_title.text)
rtemp.write("\n")
rtemp.write("## Description\n")
rtemp.write("What you should learn from this project:\n")

for item in prj_info_arr:
    if len(item) == 0:
        rtemp.write("{}\n".format(item))
        continue
    rtemp.write("* {}\n".format(item))

rtemp.write("\n")
rtemp.write("---\n")

sys.stdout.write("Writing task title, info, and file name... ")
try:
    count = 0
    while count < len(my_tasks_arr):
        rtemp.write("\n")
        rtemp.write("### [%s](./%s)\n" % (my_tasks_arr[count], file_name_arr[count]))
        rtemp.write("* %s\n" % task_info_arr[count])
        rtemp.write("\n")
        count += 1
    print("done...")
except IndexError:
    print("<Error: could not write tasks.>...")
    pass

rtemp.write("---\n")
rtemp.write("\n")
rtemp.write("## Author\n")
rtemp.write("* **%s** - " % github_keys["author_name"])
rtemp.write("[%s]" % github_keys["github_username"])
rtemp.write("(%s)" % github_keys["github_profile_link"])

print("All set!")
