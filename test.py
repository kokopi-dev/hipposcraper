#!/usr/bin/env python3
import scrapers

if __name__ == "__main__":
    url = "https://intranet.hbtn.io/projects/219"
    url2 = "https://intranet.hbtn.io/projects/233"
    print("Starting Hipposcraper:")
    a = scrapers.Connection(url)
    print(a.soup.find("a"))
    print(a.path)
    print(a.level)
