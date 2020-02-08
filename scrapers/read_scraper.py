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
    big_project_type = 0
    task_info = []
    readme = None

    def __init__(self, soup):
        self.soup = soup
        self.title = self.find_title()
        self.repo_name = self.find_repo_name()
        self.dir_name = self.check_big_project()
        self.prj_info = self.find_learning()
        self.file_names = self.find_files()
        self.task_names = self.find_tasks()
        self.task_info = self.find_task_de()
        self.prj_rsc = self.find_resources()

    def find_title(self):
        """Method that finds title of project"""
        prj_title = self.soup.find("h1")
        return prj_title.text

    def find_repo_name(self):
        """Method that finds the repository name"""
        r_name = self.soup.find(string=re.compile("GitHub repository: "))
        return r_name.next_element

    def check_big_project(self):
        """Method that checks if project is a big one"""
        try:
            temp = self.repo_name.find_next("li").next_element.next_element.text
            if "-" not in temp:
                raise AttributeError
            else:
                return temp
        except AttributeError:
            sys.stdout.write("\n     [ERROR] Failed to find directory,\
                             skipping directory creation... ")
            self.big_project_type = 1
            return ""

    def find_learning(self):
        """Method that finds the learning objectives"""
        try:
            h2 = self.soup.find("h2", string=re.compile("Learning Objectives"))
            lu = h2.find_next("h3").next_element.next_element.next_element
            txt= lu.text
            return txt.splitlines()
        except AttributeError:
            print("[ERROR] Failed to scrape learning objectives")
            sys.stdout.write("                         ... ")
            return ""

    def find_files(self):
        """Method that finds file names"""
        temp = []
        try:
            file_list = self.soup.find_all(string=re.compile("File: "))
            for idx in file_list:
                file_text = idx.next_sibling.text
                # Finding comma index for multiple files listed
                find_comma = file_text.find(",")
                if find_comma != -1:
                    temp.append(file_text[:find_comma])
                else:
                    temp.append(file_text)
            return temp
        except (IndexError, AttributeError):
            print("[ERROR] Failed to scrape file names")
            sys.stdout.write("                         ... ")
            return None

    def find_tasks(self):
        """Method that finds task names"""
        temp = []
        try:
            task_list = self.soup.find_all("h4", class_="task")
            for idx in task_list:
                item = idx.next_element.strip("\n").strip()
                temp.append(item)
            return temp
        except (IndexError, AttributeError):
            print("[ERROR] Failed to scrape task titles")
            sys.stdout.write("                         ... ")
            return None

    def find_task_de(self):
        """Method that finds the task descriptions"""
        temp = []
        try:
            info_list = self.soup.find_all(string=lambda text: isinstance
                                           (text, Comment))
            for comments in info_list:
                if comments == " Task Body ":
                    info_text = comments.next_element.next_element.text
                    temp.append(info_text.encode('utf-8'))
            return temp
        except (IndexError, AttributeError):
            print("[ERROR] Failed to scrape task descriptions")
            print("                         ... ")
            return None

    def find_resources(self):
        """Method that finds the resources"""
        try:

            h2 = self.soup.find("h2", string=re.compile("Resources"))
            p = h2.find_next("p")
            ul = p.findNext('ul')
            urls = []
            names = []
            for item in ul.find_all("a", href=True):
                url = item['href']
                name = item.text
                if (url.startswith('/rltoken/')):
                    url = 'https://intranet.hbtn.io'+ url
                urls.append(url)
                names.append(name)
            links = [names, urls]
            return links
        except AttributeError:
            print("[ERROR] Failed to scrape resources")
            sys.stdout.write("                         ... ")
            return ""

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
        self.readme.write("## Learning Objectives:bulb:\n")
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
        if (self.task_names is not None and self.file_names is not None and
            self.task_info is not None):
            sys.stdout.write("  -> Writing task information... ")
            count = 0
            while count < len(self.task_names):
                try:
                    self.readme.write("\n")
                    self.readme.write("### [{}](./{})\n".format(
                                      self.task_names[count], self.file_names[count]))
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

    def write_rsc(self):
        """Method that writes project info to README.md"""
        sys.stdout.write("  -> Writing resources... ")
        self.readme.write("## Resources:books:\n")
        self.readme.write("Read or watch:\n")
        try:
            a = self.prj_rsc
            l = len(a[0])
            for idx in range(l):
                if len(a[0][idx]) == 0:
                    self.readme.write("{}".format(a[0][idx].encode('utf-8')))
                    self.readme.write("{}\n".format(a[1][idx].encode('utf-8')))
                    continue
                self.readme.write("* [{}]".format(a[0][idx].encode('utf-8')))
                self.readme.write("({})\n".format(a[1][idx].encode('utf-8')))

            print("done")
        except (AttributeError, IndexError, UnicodeEncodeError):
            print("\n     [ERROR] Failed to write resources.")
            pass
        self.readme.write("\n")
        self.readme.write("---\n")

