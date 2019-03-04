#!/usr/bin/env python2
"""Unittest for LowScraper"""
import unittest
from scrapers import *

class TestBaseParse(unittest.TestCase):
    """Test for LowScraper"""

    def setUp(self):
        self.parse = BaseParse("https://intranet.hbtn.io/projects/232")
        self.parse.get_json()

    def tearDown(self):
        del self.parse

    def test_base_object(self):
        self.assertIsNotNone(self.parse)
        self.assertIsInstance(self.parse, object)
        self.assertIn("scrapers.base_parse.BaseParse", str(self.parse))

    def test_json_data(self):
        self.assertIsInstance(self.parse.json_data, dict)

    def test_get_soup(self):
        self.parse.get_soup()
        self.assertIsNotNone(self.parse.soup)
        self.assertIsInstance(self.parse.soup, object)
        self.assertIn("bs4.BeautifulSoup", str(self.parse.soup.__class__))
