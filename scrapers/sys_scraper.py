#!/usr/bin/env python2
"""Module for SysScraper"""
from scrapers import *


class SysScraper:
    """SysScraper class

    System-Engineering_Devops project scraper.

    Args:
        soup (obj): BeautifulSoup obj containing parsed link

    Attributes:
        ruby_check (str): if ruby exists, assign to 0. Else scrape empty list
        file_names (list): scraped file names from find_files()
    """

    ruby_check = ""
    file_names = None

    def __init__(self, soup):
        self.soup = soup

    def ruby_checker(self):
        """Method that checks for ruby files in project
        """
        self.ruby_check = self.soup.find_all(string=re.compile("env ruby"))
        if self.ruby_check != []:
            self.ruby_check = 0

    def find_files(self):
        """Method that scrapes bash or ruby for file names"""
        self.file_names = self.soup.find_all(string=re.compile("File: "))

    def write_files(self):
        """Method that writes/creates bash or ruby files"""
        sys.stdout.write("  -> Creating task files... ")
        for item in self.file_names:
            try:
                w_file_name = open(item.next_sibling.text, "w")
                if self.ruby_check == 0:
                    w_file_name.write("#!/usr/bin/env ruby\n")
                else:
                    w_file_name.write("#!/usr/bin/env bash\n")
                w_file_name.close()
            except (AttributeError, IndexError):
                sys.stdout.write("[ERROR] Failed to create ")
                sys.stdout.write("task file %s\n" % item.next_sibling.text)
                sys.stdout.write("                        ... ")
                continue
        print("done")
