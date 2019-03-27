#!/usr/bin/env python2
"""Module for ReadScraper"""
from scrapers import *
from bs4 import Comment


class ReadScraper:
    """ReadScraper class

    README.md scraper

    Args:
        soup (obj): BeautifulSoup obj containing parsed link

    Attributes:
        title (str):
        repo_name ():
        dir_name ():
    """

    title = ""
    repo_name = None
    dir_name = ""
    big_project_type = 0
    prj_info = None
    file_names = []
    task_names = []
    task_info = []
    readme = None

    def __init__(self, soup):
        self.soup = soup

    def find_title(self):
        """Method that finds title of project"""
        prj_title = self.soup.find("h1")
        self.title = prj_title.text

    def find_repo_name(self):
        """Method that finds the repository name"""
        r_name = self.soup.find(string=re.compile("GitHub repository: "))
        self.repo_name = r_name.next_element

    def check_big_project(self):
        """Method that checks if project is a big one"""
        try:
            self.dir_name = self.repo_name.find_next("li").next_element.next_element.text
            if "-" not in self.dir_name:
                raise AttributeError
        except AttributeError:
            sys.stdout.write("\n     [ERROR] Failed to find directory, skipping directory creation... ")
            self.big_project_type = 1

    def find_learning(self):
        """Method that finds the learning objectives"""
        try:
            find_prj_info = self.soup.find("h2", string=re.compile("Learning Objectives"))
            prj_info_t = find_prj_info.find_next("h3").next_element.next_element.next_element.text
            self.prj_info = prj_info_t.splitlines()
        except AttributeError:
            print("[ERROR] Failed to scrape learning objectives")
            sys.stdout.write("                         ... ")
            self.prj_info = ""
            pass

    def find_files(self):
        """Method that finds file names"""
        try:
            file_list = self.soup.find_all(string=re.compile("File: "))
            for idx in file_list:
                file_text = idx.next_sibling.text
                # Finding comma index for multiple files listed
                find_comma = file_text.find(",")
                if find_comma != -1:
                    self.file_names.append(file_text[:find_comma])
                else:
                    self.file_names.append(file_text)
        except (IndexError, AttributeError):
            print("[ERROR] Failed to scrape file names")
            sys.stdout.write("                         ... ")
            self.file_names = None
            pass

    def find_tasks(self):
        """Method that finds task names"""
        try:
            task_list = self.soup.find_all("h4", class_="task")
            for idx in task_list:
                item = idx.next_element.strip("\n").strip()
                self.task_names.append(item)
        except (IndexError, AttributeError):
            print("[ERROR] Failed to scrape task titles")
            sys.stdout.write("                         ... ")
            self.task_names = None
            pass

    def find_task_de(self):
        """Method that finds the task descriptions"""
        try:
            info_list = self.soup.find_all(string=lambda text: isinstance(text, Comment))
            for comments in info_list:
                if comments == " Task Body ":
                    info_text = comments.next_element.next_element.text
                    self.task_info.append(info_text.encode('utf-8'))
        except (IndexError, AttributeError):
            print("[ERROR] Failed to scrape task descriptions")
            print("                         ... ")
            self.task_info = None
            pass

    def open_readme(self):
        """Method that opens the README.md file"""
        try:
            if self.big_project_type == 1:
                raise IOError
            filename = self.dir_name + "/README.md"
            self.readme = open(filename, "w+")
        except IOError:
            self.readme = open("README.md", "w")

    def write_title(self):
        """Method that writes the title to README.md"""
        sys.stdout.write("  -> Writing project title... ")
        self.readme.write("# {}\n".format(self.title))
        self.readme.write("\n")
        print("done")

    def write_info(self):
        """Method that writes project info to README.md"""
        sys.stdout.write("  -> Writing learning objectives... ")
        self.readme.write("## Description\n")
        self.readme.write("What you should learn from this project:\n")
        try:
            for item in self.prj_info:
                if len(item) == 0:
                    self.readme.write("{}\n".format(item.encode('utf-8')))
                    continue
                self.readme.write("* {}\n".format(item.encode('utf-8')))
            print("done")
        except (AttributeError, IndexError, UnicodeEncodeError):
            print("\n     [ERROR] Failed to write learning objectives.")
            pass
        self.readme.write("\n")
        self.readme.write("---\n")

    def write_tasks(self):
        """Method that writes the entire tasks to README.md"""
        if (self.task_names is not None and
            self.file_names is not None and
            self.task_info is not None):
            sys.stdout.write("  -> Writing task information... ")
            count = 0
            while count < len(self.task_names):
                try:
                    self.readme.write("\n")
                    self.readme.write("### [{}](./{})\n"
                               .format(self.task_names[count], self.file_names[count]))
                    self.readme.write("* {}\n".format(self.task_info[count]))
                    self.readme.write("\n")
                    count += 1
                except IndexError:
                    sys.stdout.write("\n     [ERROR] Could not write task {}... "
                                    .format(self.task_names[count]))
                    count += 1
                    continue
            print("done")

    def write_footer(self, author, user, git_link):
        """Method that writes the footer to README.md"""
        sys.stdout.write("  -> Writing author information... ")
        self.readme.write("---\n")
        self.readme.write("\n")
        self.readme.write("## Author\n")
        self.readme.write("* **{}** - ".format(author))
        self.readme.write("[{}]".format(user))
        self.readme.write("({})".format(git_link))
        print("done")

