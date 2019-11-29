#!/usr/bin/env python3
"""Reading and writing to json data."""
import json
import os
ABSPATH = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = os.path.join(ABSPATH, ".settings.json")
CHROMEDRIVER = os.path.join(ABSPATH, "chromedriver")


def generate_settings():
    intra_email = input("What is your intranet email?\n  ")
    intra_pass = input("What is your intranet password?\n  ")
    author_name = input("What is your full name?\n  ")
    author_github_url = input("What is your github url?\n  ")
    author_github_user = input("What is your github username?\n  ")

    data = {
            "chromepath": os.path.join(os.getcwd(), "chromedriver"),
            "putcharpath": os.path.join(os.getcwd(), "_putchar.c"),
            "intra_email": intra_email,
            "intra_pass": intra_pass,
            "author_name": author_name,
            "author_github_url": author_github_url,
            "author_github_user": author_github_user,
            "setuped": False
           }
    return data

def read(filename):
    """Reads a json file and returns it in a dict.
    Args:
        filename (str): Full file path.
    """
    data = None
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    elif filename == SETTINGS_FILE:
        with open(filename, "w+") as f:
            data = generate_settings()
            json.dump(data, f)
    return data

def write(data, filename):
    if os.path.isfile(filename):
        with open(filename, "w+") as f:
            json.dump(data, f)
            return data
    return None
