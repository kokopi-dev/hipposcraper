#!/usr/bin/env python2
"""Main entry point for hipporead

Usage:
    `./hipporead.py https://intranet.hbtn.io/projects/232`
"""
from scrapers import *


def get_args():
    """Method that grabs argv

    Returns:
        link (str): argv[1]
    """
    arg = sys.argv[1:]
    count = len(arg)

    if count > 1:
        print("[ERROR] Too many arguments (must be one)")
        sys.exit()
    elif count == 0:
        print("[ERROR] Too few arguments (must be one)")
        sys.exit()

    link = sys.argv[1]
    return link

def hipporead():
    """Entry point for hipporeader

    Scrapes for specific text to create a README automatically.
    """

    link = get_args()
    parse_data = BaseParse(link)
    parse_data.get_json()

    print("Creating README.md file:")
    soup = parse_data.get_soup()

    sys.stdout.write("  -> Scraping information... ")
    # Creating scraping object
    r_scraper = ReadScraper(soup)

    # Scraping necessary data
    r_scraper.find_title()
    r_scraper.find_repo_name()
    r_scraper.find_learning()
    r_scraper.find_files()
    r_scraper.find_tasks()
    r_scraper.find_task_de()
    r_scraper.check_big_project()
    print("done")

    # Writing to README.md with scraped data
    r_scraper.open_readme()
    r_scraper.write_title()
    r_scraper.write_info()
    r_scraper.write_tasks()

    author = str(parse_data.json_data["author_name"])
    user = str(parse_data.json_data["github_username"])
    git_link = str(parse_data.json_data["github_profile_link"])

    r_scraper.write_footer(author, user, git_link)

    print("README.md all set!")

hipporead()
