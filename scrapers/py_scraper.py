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
    new_dir_files = []
    file_idx = 0
    one_dir_only = 0
    for li in find_file_name:
        text_file = li.next_sibling.text
        try:
            find_pyfile = text_file.find(".py")
            find_comma = re.search('(.+?),', text_file)

            # Creating sub directories if exists
            find_folder = re.search(', (.+?)/', text_file)

            find_dir_file = re.search('/(.+?)$', text_file)
            if find_dir_file is not None:
                new_dir_files.append(str(find_dir_file.group(1)))
            if find_folder is not None and one_dir_only is 0:
                folder_name = str(find_folder.group(1))
                os.mkdir(folder_name)
                one_dir_only += 1
            # Handling multiple files
            if "," in text_file:
                create_name = str(find_comma.group(1))
                make_comma = open(create_name, "w+")
                make_comma.close()
            elif "." not in text_file and one_dir_only is not 1:
                os.mkdir(text_file)
            else:
                make_file = open(text_file, "w+")
                make_file.write("#!/usr/bin/python3\n")
                # Creating prototypes in parallel with files
                if find_pyfile != -1:
                    make_file.write(py_proto_arr[file_idx])
                    file_idx += 1
                else:
                    pass
                make_file.close()
        except AttributeError:
            sys.stdout.write("[ERROR] Failed to create ")
            sys.stdout.write("task file %s\n" % text_file)
            sys.stdout.write("                        ... ")
            continue
        except IOError:
            sys.stdout.write("[ERROR] Failed to make file, passing\n")
            sys.stdout.write("                        ... ")
            pass
        except IndexError:
            pass

    # Making new dir files
    if folder_name is not None and one_dir_only is 1:
        os.chdir(folder_name)
        for item in new_dir_files:
            if "," in item:
                item_obj = re.search('/(.+?)$', text_file)
                item = str(item_obj.group(1))
            dir_file = open(item, "w+")
            dir_file.close()
        os.chdir("..")
