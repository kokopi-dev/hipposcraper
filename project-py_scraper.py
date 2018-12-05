import os, sys, re, string, json
import urllib2, cookielib, mechanize
from bs4 import BeautifulSoup

# Parses a webpage and returns the html
def scrape_page(link):
    page = urllib.urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')
    return soup

# Global variables
current_path = os.path.dirname(os.path.abspath(__file__))

# Command Line Arguments
arg = sys.argv[1:]
count = len(arg)

# Argument Checker
valid_link = 'intranet.hbtn.io/projects'

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

br.select_form(nr=0)
br.form['user[login]'] = intra_keys["intra_user_key"]
br.form['user[password]'] = intra_keys["intra_pass_key"]

br.submit()

my_keys.close()

# Parsing page into html soup
page = br.open(link)
soup = BeautifulSoup(page, 'html.parser')

# Making directory & changing to it
find_dir = soup.find(string=re.compile("Directory: "))
dir_name = find_dir.next_element.text
os.mkdir(dir_name)
os.chdir(dir_name)

# Creating file(s)
find_file_name = soup.find_all(string=re.compile("File: "))
for li in find_file_name:
    text_file = li.next_sibling.text
    find_comma = text_file.find(",")
    # Handling multiple files
    if find_comma != -1:
        make_comma1 = open(text_file[:find_comma], "w+")
        make_comma2 = open(text_file[find_comma:].strip(", "), "w+")
        make_comma1.close()
        make_comma2.close()
    else:
        make_file = open(text_file, "w+")
        make_file.write("#!/usr/bin/python3")
        make_file.close()

# Giving permissions to .py files
os.system("chmod u+x *.py")
