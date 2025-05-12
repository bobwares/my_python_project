#!/usr/bin/env python3
"""
File: test_slugify.py
Description: Unit tests for the slugify function.
Author: You <you@example.com>
Version: 1.0.0
"""

import unittest
from util.slugify import slugify


class TestSlugify(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_multiple_underscores(self):
        self.assertEqual(slugify("___Fancy_Title___"), "fancy-title")

    def test_spaces_and_punctuation(self):
        self.assertEqual(slugify("This is... a test!"), "this-is-a-test")

    def test_only_special_characters(self):
        self.assertEqual(slugify("@@@@"), "")

    def test_trailing_leading_spaces(self):
        self.assertEqual(slugify("   Hello  World   "), "hello-world")

    def test_mixed_case_and_symbols(self):
        self.assertEqual(slugify("Python_3.11_Rocks!"), "python-311-rocks")

    def test_empty_string(self):
        self.assertEqual(slugify(""), "")

    def test_numeric(self):
        self.assertEqual(slugify("123 456_789"), "123-456-789")


if __name__ == "__main__":
    unittest.main()
