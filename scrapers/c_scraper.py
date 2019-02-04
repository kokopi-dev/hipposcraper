#!/usr/bin/env python2
"""Defines functions for scraping C projects.

scrape_putchar - Creates _putchar file
scrape_c - Creates task files
scrape_header - Creates header file
"""
import sys


def scrape_putchar(find_putchar):
    """Create the _putchar file.

    Only writes _putchar if listed in the project description.

    Args:
        find_putchar (str): Scraped _putchar information.
    """
    # Find if page has _putchar
    find_putchar_name = find_putchar.next_sibling.text
    # Making _putchar
    if find_putchar_name == "_putchar" and find_putchar_name is not None:
        h_putchar = open("_putchar.c", "w+")
        h_putchar.write("#include <unistd.h>\n")
        h_putchar.write("\n")
        h_putchar.write("/**\n")
        h_putchar.write(" * _putchar - writes the character c to stdout\n")
        h_putchar.write(" * @c: The character to print\n")
        h_putchar.write(" *\n")
        h_putchar.write(" * Return: On success 1.\n")
        h_putchar.write(" * On error, -1 is returned, and errno")
        h_putchar.write(" is set appropriately.\n")
        h_putchar.write(" */\n")
        h_putchar.write("int _putchar(char c)\n")
        h_putchar.write("{\n")
        h_putchar.write("       return (write(1, &c, 1));\n")
        h_putchar.write("}")
        h_putchar.close()
        print("created")
    else:
        print("not created")


def scrape_c(find_file_name, get_header_name, proto_store):
    """Create task files for C projects.

    Writes header inclusion, documentation template, and
    function prototypes into files.

    Args:
        find_file_name (list): A list of task file names.
        get_header_name (str): The name of the project header file.
        proto_store (list): A list of task function prototypes.
    """
    i = 0

    for li in find_file_name:
        # Text format for file name
        file_text = li.next_sibling.text
        # Breaks icase more function names over file names
        if proto_store != 0:
            if (i == len(proto_store)):
                break

        try:
            # Pulling out name of function for documentation
            if proto_store != 0:
                func_name = proto_store[i]
                func_name = func_name.split("(", 1)[0]
                tmp_split = func_name.split(" ")
                func_name = tmp_split[len(tmp_split) - 1]
                tmp_split = func_name.split("*")
                func_name = tmp_split[len(tmp_split) - 1]

            # Removing string after first comma (multiple file names)
            find_comma = file_text.find(",")
            if find_comma != -1:
                store_file_name = open(file_text[:find_comma], "w+")
            else:
                store_file_name = open(file_text, "w+")
            if proto_store != 0:
                store_file_name.write('#include "%s"\n\n' % get_header_name)
                store_file_name.write("/**\n")
                store_file_name.write(" * %s -\n" % func_name)
                store_file_name.write(" *\n")
                store_file_name.write(" * Return: \n")
                store_file_name.write(" */\n")
                store_file_name.write("%s\n" % proto_store[i])
                store_file_name.write("{\n")
                store_file_name.write("\n")
                store_file_name.write("}")
                store_file_name.close()
            i += 1
        except (AttributeError, IndexError):
            sys.stdout.write("[ERROR] Failed to create ")
            sys.stdout.write("task file %s\n" % file_text)
            sys.stdout.write("                        ... ")
            continue


def scrape_header(find_proto_h, get_header_name, find_putchar):
    """Create header file for C projects.

    Writes include guards and function prototypes.

    Args:
        find_proto_h (list): A list of project function prototypes.
        get_header_name (str): The name of the project header file.
        find_putchar (str): Scraped _putchar information.
    """
    proto_h_store = []
    n = 0

    # Stores prototypes into a list
    for li in find_proto_h:
        proto_h_store.append(li.next_sibling.text)

    # Making header include guard string
    include_guard = get_header_name
    include_guard = include_guard.replace('.', '_', 1)
    include_guard = include_guard.upper()

    # Making header file
    sys.stdout.write("  -> Creating header file... ")
    try:
        make_header = open(get_header_name, "w+")
        make_header.write('#ifndef %s\n' % include_guard)
        make_header.write('#define %s\n' % include_guard)
        make_header.write("\n")
        make_header.write("#include <stdio.h>\n")
        make_header.write("#include <stdlib.h>\n")
        make_header.write("\n")

        try:
            if len(find_putchar) == 23:
                make_header.write("int _putchar(char c);\n")
        except TypeError:
            pass

        for li in find_proto_h:
            if n == len(proto_h_store):
                break
            make_header.write(proto_h_store[n])
            make_header.write("\n")
            n += 1

        make_header.write("\n")
        make_header.write('#endif /* %s */' % include_guard)
        make_header.close()
        print("done")

    except AttributeError:
        print("[ERROR] Failed to create header file")
