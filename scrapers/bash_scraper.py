#!/usr/bin/python2
import sys

def scrape_bash(find_file_name):
    for li in find_file_name:
        try:
            make_file = open(li.next_sibling.text, "w+")
            make_file.write("#!/usr/bin/env bash\n")
            make_file.close()
        except:
            sys.stdout.write("Error: Could not create ")
            sys.stdout.write("task file %s\n" % text_file)
            sys.stdout.write("                   ... ")
            continue

