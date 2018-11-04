import os
import urllib2
import cookielib
import mechanize
import sys
import re
import json
import string
from bs4 import BeautifulSoup

# Parses a webpage and returns the html
def scrape_page(link):
        page = urllib.urlopen(link)
        soup = BeautifulSoup(page, 'html.parser')
        return soup

# Command Line Arguments
arg = sys.argv[1:]
count = len(arg)

# Argument Limiter
# Change to 3 after finishing _putchar option
if count != 2:
        print("Enter in project url only, followed by header file name, followed by 'y' or 'n'.")
        sys.exit()

# _putchar option variable

# Intranet login credentials
with open("/CHANGE_TO_YOUR_DIRECTORY_HERE/auth_data.json", "r") as my_keys:
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

# Making directory & changing to it
find_dir = soup.find(string=re.compile("Directory: "))
dir_name = find_dir.next_element.text
os.mkdir(dir_name)
os.chdir(dir_name)

# Making _putchar

# Variables for function name array
proto_store = []
i = 0

# Making function name array
find_proto = soup.find_all(string=re.compile("Prototype: "))
for li in find_proto:
		proto_store.append(li.next_sibling.text.replace(";", ""))

# Making C files with function name array
find_file_name = soup.find_all(string=re.compile("File: "))
for li in find_file_name:
	if (i == len(proto_store)):
		break;
        store_file_name = open(li.next_sibling.text, "w+")
        store_file_name.write('#include "%s"\n\n' % sys.argv[2])
        store_file_name.write("/**\n")
        store_file_name.write(" * main - Entry Point\n")
	store_file_name.write(" *\n")
	store_file_name.write(" * Return:\n")
	store_file_name.write(" */\n")
	store_file_name.write("%s\n" % proto_store[i])
	store_file_name.write("{\n")
	store_file_name.write("\n")
	store_file_name.write("}")
	i += 1
store_file_name.close()

# Variables for header prototypes array
proto_h_store = []
n = 0

# Find header prototype
find_proto_h = soup.find_all(string=re.compile("Prototype: "))
for li in find_proto_h:
        proto_h_store.append(li.next_sibling.text)

# Making header include guard string
include_guard = sys.argv[2]
include_guard = include_guard.replace('.', '_', 1)
include_guard = include_guard.upper()

# Making header file
make_header = open(sys.argv[2], "w+")
make_header.write('#ifndef %s\n' % include_guard)
make_header.write('#define %s\n' % include_guard)
make_header.write("\n")
make_header.write("\n")
# If statement for _putchar option
make_header.write("int _putchar(char c);\n")

for li in find_proto_h:
        if (n == len(proto_h_store)):
                break;
        make_header.write(proto_h_store[n])
        make_header.write("\n")
        n += 1

make_header.write("\n")
make_header.write('#endif /* %s */' % include_guard)
make_header.close()

# Making README
