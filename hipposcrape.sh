#!/usr/bin/env bash
# Run the Holberton project scraper on a link to a Holberton project.
#   The first argument provided to the script is expected to be a
#+  link to a Holberton School project.

project=$1
python2 ENTER_FULL_PATHNAME_TO_DIRECTORY_HERE/project-all_scraper.py "$project"
python2 ENTER_FULL_PATHNAME_TO_DIRECTORY_HERE/holberton-read_t.py "$project"
