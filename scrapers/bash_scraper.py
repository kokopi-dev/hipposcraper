#!/usr/bin/env python2 
"""Defines the file creator for system engineering projects."""
import sys


def scrape_bash(find_file_name):
    """Create Bash script files for system engineering projects.

    Files are created with shebangs.

    Args:
        find_file_name (list): A list of task file names.
    """
    for li in find_file_name:
        try:
            make_file = open(li.next_sibling.text, "w")
            make_file.write("#!/usr/bin/env bash\n")
            make_file.close()
        except (AttributeError, IndexError):
            sys.stdout.write("[ERROR] Failed to create ")
            sys.stdout.write("task file %s\n" % text_file)
            sys.stdout.write("                        ... ")
            continue
