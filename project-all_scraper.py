#!/usr/bin/python2
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
    print("  <Error: Too many arguments (must be one)>")
    sys.exit()
elif count == 0:
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

sys.stdout.write("Logging in and opening project... ")
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

    print("done.")

except:
    print("Error: Could not log in -",
          "did you set your login keys in auth_data.json?")
    sys.exit()

# ------------------------------
# --- Python Project Scraper ---
# ------------------------------
if find_project_type == "holbertonschool-higher_level_programming":
    # Making and changing to proper directory
    sys.stdout.write("Creating directory... ")
    try:
        os.mkdir(dir_name)
        os.chdir(dir_name)
        print("done.")
    except:
        print("Error: Could not create directory - "
              "does the directory already exist?")
        sys.exit()

    # Creating file(s) from scrapers.py_scraper
    sys.stdout.write("Creating task files... ")
    find_file_name = soup.find_all(string=re.compile("File: "))
    py_proto_tag = soup.find_all(string=re.compile("Prototype: "))
    scrape_py(find_file_name, py_proto_tag)
    print("done.")

    # Finding and making py main files
    sys.stdout.write("Creating test files... ")
    find_pre = soup.select("pre")
    scrape_tests(find_pre)
    print("done.")

    # Giving permissions to .py files
    sys.stdout.write("Setting permissions... ")
    try:
        os.system("chmod u+x *.py")
        print("done.")
    except:
        print("Error: Could not set permissions.")

    print("All set!")

# -------------------------
# --- C Project Scraper ---
# -------------------------
elif find_project_type == "holbertonschool-low_level_programming":
    # Making and changing to proper directory
    sys.stdout.write("Creating directory... ")
    try:
        os.mkdir(dir_name)
        os.chdir(dir_name)
        print("done.")
    except:
        print("Error: Could not create directory.")
        sys.exit()

    # Setting _putchar variables and scraping it
    sys.stdout.write("Checking for _putchar... ")
    find_putchar = soup.find(string=re.compile("You are allowed to use"))
    find_putchar_name = ""
    scrape_putchar(find_putchar, find_putchar_name)

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
        i = 0

        # Making function name array
        find_proto = soup.find_all(string=re.compile("Prototype: "))
        for li in find_proto:
            proto_store.append(li.next_sibling.text.replace(";", ""))

        # Making C files with function name array
        sys.stdout.write("Creating task files... ")
        find_file_name = soup.find_all(string=re.compile("File: "))
        for li in find_file_name:
            # Text format
            file_text = li.next_sibling.text
            # Breaks incase more function names over file names
            if (i == len(proto_store)):
                break

            try:
                # Pulling out name of function for documentation
                func_name = proto_store[i]
                func_name = func_name.split("(", 1)[0]
                tmp_split = func_name.split(" ")
                func_name = tmp_split[len(tmp_split) - 1]
                tmp_split = func_name.split("*")
                func_name = tmp_split[len(tmp_split) - 1]

                # Removing string after first comma (multiple file names)
                find_comma = file_text.find(",")
                if find_comma != -1:
                    store_file_name = open(file_text[:find_comma], "w+")
                else:
                    store_file_name = open(file_text, "w+")
                store_file_name.write('#include "%s"\n\n' % get_header_name)
                store_file_name.write("/**\n")
                store_file_name.write(" * %s -\n" % func_name)
                store_file_name.write(" *\n")
                store_file_name.write(" * Return: \n")
                store_file_name.write(" */\n")
                store_file_name.write("%s\n" % proto_store[i])
                store_file_name.write("{\n")
                store_file_name.write("\n")
                store_file_name.write("}")
                store_file_name.close()
                i += 1
            except:
                sys.stdout.write("Error: Could not create ")
                sys.stdout.write("task file %s\n" % file_text)
                sys.stdout.write("                   ... ")
                continue

        print("done.")

        # Variables for header prototypes array
        proto_h_store = []
        n = 0

        # Find header prototype
        find_proto_h = soup.find_all(string=re.compile("Prototype: "))
        for li in find_proto_h:
                proto_h_store.append(li.next_sibling.text)

        # Making header include guard string
        include_guard = get_header_name
        include_guard = include_guard.replace('.', '_', 1)
        include_guard = include_guard.upper()

        # Making header file
        sys.stdout.write("Creating header file... ")
        try:
            make_header = open(get_header_name, "w+")
            make_header.write('#ifndef %s\n' % include_guard)
            make_header.write('#define %s\n' % include_guard)
            make_header.write("\n")
            make_header.write("#include <stdio.h>\n")
            make_header.write("#include <stdlib.h>\n")
            make_header.write("\n")

            if find_putchar_name == "_putchar" and find_putchar is not None:
                make_header.write("int _putchar(char c);\n")

            for li in find_proto_h:
                if n == len(proto_h_store):
                    break
                make_header.write(proto_h_store[n])
                make_header.write("\n")
                n += 1

            make_header.write("\n")
            make_header.write('#endif /* %s */' % include_guard)
            make_header.close()
            print("done.")

        except:
            print("Error: Could not create header file.")

    else:
        # Making C files with function name array
        sys.stdout.write("Creating task files... ")
        find_file_name = soup.find_all(string=re.compile("File: "))
        scrape_c(find_file_name)
        print("done.")

    # Finding and making c main files
    sys.stdout.write("Creating test files... ")
    find_pre = soup.select("pre")
    scrape_tests(find_pre)
    print("done.")

    # Giving permissions to .c files
    sys.stdout.write("Setting permissions... ")
    try:
        os.system("chmod u+x *.c")
        print("done.")
    except:
        print("Error: Could not set permissions.")

    print("All set!")

else:
    print("Fatal Error: Could not find project's type\n")
    exit(1)
