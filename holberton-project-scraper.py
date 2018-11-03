import sys
import re
import json
from bs4 import BeautifulSoup

# fill in prototype in each file
# create all files in x project website

# Parses a webpage and returns the html
def scrape_page(link):
        page = urllib.urlopen(link)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

# Command Line Arguments
arg = sys.argv[1:]
count = len(arg)

# Argument Limiter
if count != 1:
        print("Enter in project website link only.")
        sys.exit()

# Intranet login credentials
with open("auth_data.json", "r") as my_keys:
        intra_keys = json.load(my_keys)


# Login Variables
link = sys.argv[1]
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


# loop through file:
# project_file_name = code
# open(project_file_name, "w+")
#find_proto_h = soup.find_all(string=re.compile("Prototype: "))

#for li in find_proto_h:
#       print(li.next_sibling.text)

proto_store = []
i = 0

# Stores C file prototypes into array
find_proto = soup.find_all(string=re.compile("Prototype: "))
for li in find_proto:
		proto_store.append(li.next_sibling.text.replace(";", ""))

# Loop that creates files with names & fills in prototypes
find_file_name = soup.find_all(string=re.compile("File: "))
for li in find_file_name:
        store_file_name = open(li.next_sibling.text, "w+")                                                           
        store_file_name.write('#include "holberton.h"\n')
        store_file_name.write("/**\n")
        store_file_name.write(" * main - Entry Point\n")   
        store_file_name.write(" * Return: 0\n")
        store_file_name.write(" */\n")
        store_file_name.write("%s\n" % proto_store[i])
        store_file_name.write("{\n")
        store_file_name.write("\n")
        store_file_name.write("}")
        i += 1
