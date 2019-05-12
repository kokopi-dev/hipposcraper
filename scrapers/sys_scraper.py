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

    def __init__(self, soup):
        self.soup = soup
        self.file_names = self.find_files()
        self.ruby_check = self.ruby_checker()

    def ruby_checker(self):
        """Method that checks for ruby files in project
        """
        temp = self.soup.find_all(string=re.compile("env ruby"))
        if temp != []:
            return = 0
        else:
            return temp

    def find_files(self):
        """Method that scrapes bash or ruby for file names"""
        return self.soup.find_all(string=re.compile("File: "))

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
                try:
                    sys.stdout.write("task file %s\n" % item.next_sibling.text)
                except AttributeError:
                    sys.stdout.write("any task files, tasks do not exist\n")
                sys.stdout.write("                        ... ")
                continue
        print("done")
