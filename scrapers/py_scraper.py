#!/usr/bin/env python2
"""Defines Python file creation function."""
import sys
import re
import os


def scrape_py(find_file_name, py_proto_tag):
    """Scrape Python project files.

    Writes shebang and function prototypes to each file.

    Args:
        find_file_name (list): A list of project file names.
        py_proto_tag (str): Scraped function prototypes.
    """
    # Storing py prototypes into arr
    py_proto_arr = []
    for item in py_proto_tag:
        py_proto = item.next_sibling.text
        find_py = py_proto.find(":")
        # Stores only python prototypes
        if find_py != -1:
            py_proto_arr.append(py_proto)
        else:
            pass

    file_idx = 0
    for li in find_file_name:
        text_file = li.next_sibling.text
        try:
            find_comma = re.search('(.+?),', text_file)
            find_pyfile = text_file.find(".py")
            # Creating sub directories if exists
            oneDirectoryOnly = 0
            find_folder = re.search(', (.+?)/', text_file)
            if find_folder is not None and oneDirectoryOnly is 0:
                folder_name = str(find_folder.group(1))
                os.mkdir(folder_name)
                oneDirectoryOnly += 1
            # Handling multiple files
            if "," in text_file:
                create_name = str(find_comma.group(1))
                make_comma = open(create_name, "w+")
                make_comma.close()
            else:
                make_file = open(text_file, "w+")
                make_file.write("#!/usr/bin/env python3\n")
                # Creating prototypes in parallel with files
                if find_pyfile != -1:
                    try:
                        make_file.write(py_proto_arr[file_idx])
                        file_idx += 1
                    except IndexError:
                        pass
                else:
                    pass
                make_file.close()
        except AttributeError:
            sys.stdout.write("[ERROR] Failed to create ")
            sys.stdout.write("task file %s\n" % text_file)
            sys.stdout.write("                        ... ")
            continue
