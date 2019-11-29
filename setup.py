#!/usr/bin/env python3
import database as db
import os

def setup():
    settings = db.read(db.SETTINGS_FILE)
    if not settings["setuped"]:
        os.system(f"./sel-setup {db.ABSPATH}")

setup()
