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

# Argument Checker
valid_link = 'intranet.hbtn.io/projects'
valid_header = '.h'

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

# Header file prompt
no_header = 0
header = raw_input("Enter name for project header file (leave empty if no header required): ")
if (header == ""):
        no_header = 1
else:
        while not (header[-2:] in valid_header):
                print("  <Error: Header file must end in .h>")
                header = raw_input("Enter name for project header file: ")

# Putchar file prompt
putchar_list = ['y', 'n'];
putchar_y_n = raw_input("Do you want to add _putchar.c? (y/n): ")
while not (putchar_y_n in putchar_list):
        print(" <Error: Enter in 'y' or 'n'>")
        putchar_y_n = raw_input("Do you want to add _putchar.c? (y/n): ")

if (putchar_y_n == 'y'):
        putchar_res = 1
if (putchar_y_n == 'n'):
        putchar_res = 0

# Intranet login credentials
with open("/home/vagrant/others/personal-scripts/personal_auth_data.json", "r") as my_keys:
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

# Making _putchar
if (putchar_res == 1):
        h_putchar = open("_putchar.c", "w+")
        h_putchar.write("#include <unistd.h>\n")
        h_putchar.write("\n")
        h_putchar.write("/**\n")
        h_putchar.write(" * _putchar - writes the character c to stdout\n")
        h_putchar.write(" * @c: The character to print\n")
        h_putchar.write(" *\n")
        h_putchar.write(" * Return: On success 1.\n")
        h_putchar.write(" * On error, -1 is returned, and errno is set appropriately.\n")
        h_putchar.write(" */\n")
        h_putchar.write("int _putchar(char c)\n")
        h_putchar.write("{\n")
        h_putchar.write("       return (write(1, &c, 1));\n")
        h_putchar.write("}")
        h_putchar.close()

if (no_header == 1):
        i = 0
        # Making C files with function name array
        find_file_name = soup.find_all(string=re.compile("File: "))
        for li in find_file_name:
                store_file_name = open(li.next_sibling.text, "w+")
                store_file_name.write("#include <stdio.h>\n")
                store_file_name.write("#include <stdlib.h>\n")
                store_file_name.write("/**\n")
                store_file_name.write(" * main - Entry Point\n")
                store_file_name.write(" *\n")
                store_file_name.write(" * Return:\n")
                store_file_name.write(" */\n")
                store_file_name.write("int main(void)\n")
                store_file_name.write("{\n")
                store_file_name.write("\n")
                store_file_name.write("}")
                store_file_name.close()
                i += 1

if (no_header == 0):
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
                store_file_name.write('#include "%s"\n\n' % header)
                store_file_name.write("/**\n")
                store_file_name.write(" * main - Entry Point\n")
                store_file_name.write(" *\n")
                store_file_name.write(" * Return:\n")
                store_file_name.write(" */\n")
                store_file_name.write("%s\n" % proto_store[i])
                store_file_name.write("{\n")
                store_file_name.write("\n")
                store_file_name.write("}")
                store_file_name.close()
                i += 1

        # Variables for header prototypes array
        proto_h_store = []
        n = 0

        # Find header prototype
        find_proto_h = soup.find_all(string=re.compile("Prototype: "))
        for li in find_proto_h:
                proto_h_store.append(li.next_sibling.text)

        # Making header include guard string
        include_guard = header
        include_guard = include_guard.replace('.', '_', 1)
        include_guard = include_guard.upper()

        # Making header file
        make_header = open(header, "w+")
        make_header.write('#ifndef %s\n' % include_guard)
        make_header.write('#define %s\n' % include_guard)
        make_header.write("\n")
        make_header.write("#include <stdio.h>\n")
        make_header.write("#include <stdlib.h>\n")
        make_header.write("\n")

        if (putchar_res == 1):
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
