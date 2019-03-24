#!/usr/bin/env python2
"""Module for TestFileScraper"""
from scrapers import *

class TestFileScraper:
    """TestFileScraper class

    Scrapes test files from any projects.

    Args:
        soup (obj): BeautifulSoup obj containing parsed link
    """

    pre = None

    def __init__(self, soup):
        self.soup = soup

    def find_test_files(self):
        self.pre = self.soup.select("pre")

    def write_test_files(self):
        sys.stdout.write("  -> Creating test files... ")
        for item in self.pre:
            find_test = item.text.find("cat")
            find_c = item.text.find("main.c")
            find_py = item.text.find(".py")

            # find_main checks if there are main files on project page
            if find_test != -1 and (find_c != -1 or find_py != -1):
                try:
                    user = item.text.split("$", 1)[0]
                    name = item.text.split("cat ", 1)[1]
                    if find_c != -1:
                        name = name.split(".c", 1)[0] + ".c"
                    else:
                        name = name.split(".py", 1)[0] + ".py"
                    text = item.text.split(name, 1)[1]
                    text = text.split("\n", 1)[1]
                    text = text.split(user, 1)[0]
                    text = text.split("\n")
                    w_test_file = open(name, "w+")
                    for i in range(len(text) - 1):
                        w_test_file.write(text[i].encode('utf-8') + "\n")
                    w_test_file.close()
                except (AttributeError, IndexError):
                    sys.stdout.write("[ERROR] Could not create ")
                    sys.stdout.write("test file %s\n" % name)
                    sys.stdout.write("                        ... ")
                    continue
                except IOError:
                    sys.stdout.write("\n     [ERROR] Could not create a specific test file.")
                    continue
            else:
                pass
        print("done")
