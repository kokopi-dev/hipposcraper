#!/usr/bin/env python2
"""Main entry point for hippoproject

Usage:
    `./hippoproject.py https://intranet.hbtn.io/projects/232`
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

def set_permissions():
    """Method that sets permissions on files"""
    sys.stdout.write("  -> Setting permissions... ")
    try:
        os.system("chmod u+x *")
        print("done")
    except OSError:
        print("[ERROR] Failed to set permissions")
    
def hippoproject():
    """Entry point for hippoproject

    Scrapes project type (low level, high level, or system engineer),
    then it checks project type to execute appropriate scrapes.
    """

    link = get_args()

    print("\nHipposcraper version 1.0.7")
    print("Creating project:")
    parse_data = BaseParse(link)

    parse_data.find_directory()
    parse_data.create_directory()

    project_type = parse_data.project_type_check()
    if "high" in project_type:
        # Creating scraping objects
        hi_scraper = HighScraper(parse_data.soup)
        t_scraper = TestFileScraper(parse_data.soup)

        # Writing to files with scraped data
        hi_scraper.write_files()

        # Creating test (main) files
        t_scraper.write_test_files()

    elif "low" in project_type:
        # Creating scraping objects
        lo_scraper = LowScraper(parse_data.soup)
        t_scraper = TestFileScraper(parse_data.soup)

        # Writing to files with scraped data
        lo_scraper.write_putchar()
        lo_scraper.write_header()
        lo_scraper.write_files()

        # Creating test (main) files
        t_scraper.write_test_files()

    elif "system" in project_type:
        # Creating scraping objects
        sy_scraper = SysScraper(parse_data.soup)
        t_scraper = TestFileScraper(parse_data.soup)

        # Creating test (main) files
        t_scraper.write_test_files()

        # Writing to files with scraped data
        sy_scraper.write_files()

    else:
        print("[ERROR]: Could not determine project type")
        sys.exit()

    set_permissions()
    print("Project all set!")

if __name__ == "__main__":
    hippoproject()
