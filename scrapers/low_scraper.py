#!/usr/bin/env python2
"""Module for LowScraper"""
from scrapers import *

class LowScraper:
    """LowParse class

    Low-Level-Programming project scraper.

    Args:
        soup (obj): BeautifulSoup obj containing parsed link
    """
    prototypes_list = []
    file_names = None
    header_check = 0
    header_name = ""
    putchar_check = ""

    def __init__(self, soup):
        """Instantiation of LowScraper"""
        self.soup = soup

    def find_putchar(self):
        sys.stdout.write("  -> Checking for _putchar... ")
        search_putchar = self.soup.find(string=re.compile("You are allowed to use"))
        try:
            if len(search_putchar) == 23:
                self.putchar_check = search_putchar.next_sibling.text
        except TypeError:
            pass

    def write_putchar(self):
        if self.putchar_check == "_putchar":
            w_putchar = open("_putchar.c", "w+")
            w_putchar.write("#include <unistd.h>\n")
            w_putchar.write("\n")
            w_putchar.write("/**\n")
            w_putchar.write(" * _putchar - writes the character c to stdout\n")
            w_putchar.write(" * @c: The character to print\n")
            w_putchar.write(" *\n")
            w_putchar.write(" * Return: On success 1.\n")
            w_putchar.write(" * On error, -1 is returned, and errno")
            w_putchar.write(" is set appropriately.\n")
            w_putchar.write(" */\n")
            w_putchar.write("int _putchar(char c)\n")
            w_putchar.write("{\n")
            w_putchar.write("       return (write(1, &c, 1));\n")
            w_putchar.write("}")
            w_putchar.close()
            print("created")
        else:
            print("not created")

    def find_prototypes(self):
        find_protos = self.soup.find_all(string=re.compile("Prototype: "))
        for item in find_protos:
            self.prototypes_list.append(item.next_sibling.text.replace(";", ""))

    def find_header(self):
        try:
            finder = "forget to push your header file"
            header_text = self.soup.find(string=re.compile(finder)).previous_element
            self.header_name = header_text.previous_element.previous_element
        except AttributeError:
            self.header_check = 1

    def write_header(self):
        if self.header_check == 0:
            # Making header include guard string
            include_guard = self.header_name
            include_guard = include_guard.replace('.', '_', 1)
            include_guard = include_guard.upper()

            sys.stdout.write("  -> Creating header file... ")
            try:
                w_header = open(self.header_name, "w+")
                w_header.write('#ifndef %s\n' % include_guard)
                w_header.write('#define %s\n' % include_guard)
                w_header.write("\n")
                w_header.write("#include <stdio.h>\n")
                w_header.write("#include <stdlib.h>\n")
                w_header.write("\n")

                try:
                    if self.putchar_check == "_putchar":
                        w_header.write("int _putchar(char c);\n")
                except TypeError:
                    pass

                n = 0
                for item in self.prototypes_list:
                    if n == len(self.prototypes_list):
                        break
                    w_header.write(self.prototypes_list[n])
                    w_header.write("\n")
                    n += 1

                w_header.write("\n")
                w_header.write('#endif /* %s */' % include_guard)
                w_header.close()
                print("done")
            except AttributeError:
                print("[ERROR] Failed to create header file")
        else:
            pass

    def find_files(self):
        self.file_names = self.soup.find_all(string=re.compile("File: "))

    def write_files(self):
        i = 0

        for item in self.file_names:
            file_text = item.next_sibling.text
            # Breaks incase more function names over file names
            if self.prototypes_list != 0:
                if (i == len(self.prototypes_list)):
                    break

            try:
                # Pulling out name of function for documentation
                if self.prototypes_list != 0:
                    func_name = self.prototypes_list[i]
                    func_name = func_name.split("(", 1)[0]
                    tmp_split = func_name.split(" ")
                    func_name = tmp_split[len(tmp_split) - 1]
                    tmp_split = func_name.split("*")
                    func_name = tmp_split[len(tmp_split) - 1]

                # Removing string after first comma (multiple file names)
                find_comma = file_text.find(",")
                if find_comma != -1:
                    w_file_name = open(file_text[:find_comma], "w+")
                else:
                    w_file_name = open(file_text, "w+")

                if self.header_check != 1:
                    w_file_name.write('#include "%s"\n\n' % self.header_name)
                    w_file_name.write("/**\n")
                    w_file_name.write(" * %s -\n" % func_name)
                    w_file_name.write(" *\n")
                    w_file_name.write(" * Return: \n")
                    w_file_name.write(" */\n")
                    w_file_name.write("%s\n" % self.prototypes_list[i])
                    w_file_name.write("{\n")
                    w_file_name.write("\n")
                    w_file_name.write("}")
                    w_file_name.close()
                i += 1
            except (AttributeError, IndexError):
                sys.stdout.write("[ERROR] Failed to create ")
                sys.stdout.write("task file %s\n" % file_text)
                sys.stdout.write("                        ... ")
                continue
