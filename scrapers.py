#!/usr/bin/env python3
import json
import re
import os
import time
import database as db
from selenium import webdriver
from requests_html import HTML
SETTINGS = db.read(db.SETTINGS_FILE)
# TODO Shared function list:
# - write_files


class Connection:
    """Create this object to do the following:
    Log into the intranet, save project HTML into soup, save project type/
    level, save project directory, create project directory.
    """
    def __init__(self, project_url):
        self.soup = self.get_project(project_url)
        self.path = self.make_path()
        self.level = self.project_type()

    def browser_settings(self):
        options = ["--incognito", "--headless", "--disable-gpu",
                   "--no-sandbox", "--disable-dev-shm-usage"]
        driver = webdriver.ChromeOptions()
        for o in options:
            driver.add_argument(o)
        return driver

    def get_project(self, project_url):
        """Login intranet, then gets project_url's HTML and saves to soup
        """
        login_url = "https://intranet.hbtn.io/auth/sign_in"
        browser = webdriver.Chrome(executable_path=SETTINGS["chromepath"],
                                   options=self.browser_settings())
        browser.get(login_url)
        browser.find_element_by_name("user[login]").send_keys(SETTINGS["intra_email"])
        browser.find_element_by_name("user[password]").send_keys(SETTINGS["intra_pass"])
        browser.find_element_by_name("commit").click()
        time.sleep(0.2)
        print("  -> Login success!")
        # TODO Create check if project page is valid
        browser.get(project_url)
        soup = HTML(html=browser.page_source)
        return soup

    def project_type(self):
        """Multithread: Finds and saves project type/level."""
        return "to do"

    def make_path(self):
        """Multithread: Finds and saves project directory, then creates it."""

        """
        if os.path.isdir(dir_path):
            print("{} folder already exists, skipping...".format(dir_path))
        else:
            os.mkdir(dir_path)
        """
        return "to do"

class LowLevel:
    def __init__(self, soup, path):
        print("  -> Creating {}:".format(path))
        self.path = path
        self.soup = soup
        self.header = None
        self.prototypes = None
        self.files = None
        """
        Run check_header, putchar, get_prototypes, get_files
        Run write_files, write_checker
        if self.header, write_header
        """

    def putchar(self):
        """Checks if _putchar.c can be used. If yes, copys _putchar.c
        to project directory.
        """
        checker = self.soup.find(string=re.compile("You are allowed to use"))
        if checker:
            print("    -> Writing _putchar.c ...", end="")
            os.system("cp {} {}".format(SETTINGS["putcharpath"], self.path))
        else:
            pass

    def check_header(self):
        checker = self.soup.find(string=re.compile("forget to push your header file"))
        if checker:
            try:
                self.header = checker.previous_element.previous_element.previous_element
            except AttributeError:
                print("(scraper.py - LowLevel) Error: Could not find header file name.")

    def get_files(self):
        data = self.soup.find_all(string=re.compile("File: "))
        res = []
        for tag in data:
            filename = tag.next_sibling.text
            if filename.find(",") != -1:
                filename = tag.split(",")[0]
            res.append(filename)
        self.files = res

    def get_prototypes(self):
        """Saves all prototypes, and then writes them"""
        prototypes = []
        data = self.soup.find_all(string=re.compile("Prototype: "))
        for tag in data:
            prototypes.append(tag.next_sibling.text.replace(";", ""))
        self.prototypes = prototypes

    def write_files(self):
        """Creates a list of function names from self.prototypes, checks for
        multi file names in self.files, writes files with appropriate content.
        """
        func_list = []
        idx = 0
        if type(self.prototypes) is list and self.prototypes[0]:
            # Splitting ; in prototypes for .c files
            for p in self.prototypes:
                name = p.split("(", 1)[0]
                tmp = name.split(" ")
                name = tmp[len(tmp) - 1]
                tmp = name.split("*")
                name = tmp[len(tmp) - 1]
                func_list.append(name)

        if type(self.files) is list and self.files[0]:
            for item in self.files:
                try:
                    path = os.path.join(self.path, item)
                    with open(path, "w") as f:
                        if self.header:
                            f.write('#include "{}"\n'.format(self.header))
                            f.write("/**\n * {} -\n".format(func_list[idx]))
                            f.write(" *\n * Return: \n */\n")
                            f.write("{}\n".format(self.prototypes[idx]))
                            f.write("{\n\n}")
                    print("    -> Created {} ...".format(item))
                except IndexError:
                    print("    -> Error: Failed to create {} ...".format(item))
                idx += 1

    def write_header(self):
        print("    -> Writing {} ...".format(self.header), end="")
        path = os.path.join(self.path, self.header)
        guard = self.header.replace(".", "_", 1).upper()
        with open(path, "w+") as f:
            f.write("#ifndef {}\n#define {}\n\n".format(guard, guard))
            f.write("#include <stdio.h>\n#include <stlib.h>\n")
            if self.prototypes[0]:
                for p in self.prototypes:
                    f.write(p + ";\n")
            f.write("#endif /* {} */".format(guard))

    def write_checker(self):
        print("    -> Writing check.sh ...")
        path = os.path.join(self.path, "check.sh")
        with open(path, "w+") as f:
            f.write("#!/usr/bin/env bash\nbetty ")
            if self.header:
                f.write('"{}" '.format(self.header))
            if type(self.files) is list:
                for item in self.files:
                    f.write('"{}" '.format(item))

'''
class HighLevel:
    """Data format (dict): {filename: {'prototype': prototype}}"""
    def __init__(self, soup, path):
        print("  -> Creating {}:".format(path))
        self.soup = soup
        self.path = path
        self.info = {}

        self.get_info()
        funcs_0 = [self.write_files, self.write_checker]
        gen_threads(funcs_0)

    def get_info(self):
        """Gets a list of each div in task section. Then gets and sorts
        filenames and prototypes. All data gets stored into self.info to
        be used in writer methods.
        """
        data = self.soup.find("section", class_="formatted-content")
        data = data.find_next("section", class_="formatted-content").find_all("div")
        for i in data:
            if i.get("data-position", None):
                testfile = i.find("pre").find("code")
                if testfile:
                    # Find test
                    if testfile.text.find("cat") != -1:
                        testname = testfile.text.split("cat ", 1)[0]
                        user = testfile.text.split("$", 1)[0]
                        if testfile.text.find(".py"):
                            testname = testname.split(".py", 1)[0] + ".py"
                        t = testfile.text.split(testname, 1)[1]
                        t = text.split("\n", 1)[1].split(user, 1)[0].split("\n")
                        print(text)
        
                filename = i.find(string=re.compile("File: "))
                if filename:
                    filename = filename.next_sibling.text
                if filename.find(",") != -1:
                    filename = filename.split(",")[0]
                prototype = i.find(string=re.compile("Prototype: "))
                if prototype:
                    prototype = prototype.next_sibling.text
                self.info[filename] = {"prototype": prototype}

    def write_files(self):
        for filename, prototype in self.info.items():
            path = os.path.join(self.path, filename)
            with open(path, "w") as f:
                if ".py" in filename:
                    f.write("#!/usr/bin/python3\n")
                    if prototype.get("prototype", None):
                        f.write(prototype["prototype"])
                if ".sh" in filename:
                    f.write("#!/usr/bin/bash\n")
                if ".js" in filename:
                    f.write("#!/usr/bin/node\n")
                print("    -> Created {} ...".format(filename))

    def write_checker(self):
        print("    -> Writing check.sh ...")
        path = os.path.join(self.path, "check.sh")
        with open(path, "w+") as f:
            if ".js" in self.info[list(self.info)[0]]:
                f.write("#!/usr/bin/env bash\nsemistandard --fix ")
            else:
                f.write("#!/usr/bin/env bash\npep8 ")
            if len(list(self.info)) > 0:
                for item in list(self.info):
                    f.write('"{}" '.format(item))

class System:
    def __init__(self, soup, path):
        print("  -> Creating {}:".format(path))
        self.soup = soup
        self.path = path

class Readme:
    def __init__(self, soup, path):
        print("    -> Creating README.md ...")
        self.soup = soup
        self.path = path
        self.info = {}
        self.find_info()
        self.write_info()

    def find_info(self):
        self.info["title"] = self.soup.find("h1")

        repo_name = self.soup.find(string=re.compile("GitHub repository: "))
        self.info["repo_name"] = repo_name.next_element

        self.info["files"] = []
        all_files = self.soup.find_all(string=re.compile("File: "))
        for tag in all_files:
            filename = tag.next_sibling.text
            if filename.find(",") != -1:
                filename = item.split(",")[0]
            self.info["files"].append(filename)

        try:
            h2_learn = self.soup.find("h2", string=re.compile("Learning Objectives"))
            h3_learn = h2_learn.find_next("h3").next_element.next_element.text
            self.info["learning"] = h3_learn
        except AttributeError:
            self.info["learning"] = ""

        self.info["tasks"] = []
        task_list = self.soup.find_all("h4", class_="task")
        for task in task_list:
            try:
                self.info["tasks"].append(task.next_element.strip("\n").strip())
            except AttributeError:
                pass

        self.info["task_desc"] = []
        desc_list = self.soup.find_all(string=lambda text: isinstance(text, Comment))
        for desc in desc_list:
            if desc == " Task Body ":
                try:
                    text = desc.next_element.next_element.text
                    self.info["task_desc"].append(text.encode("utf-8"))
                except AttributeError:
                    pass

    def write_info(self):
        path = os.path.join(self.path, "README.md")
        with open(path, "w+") as f:
            f.write("# {}\n\n".format(self.info["title"]))
            f.write("## Description\nWhat should you learn from this project:\n")
'''
