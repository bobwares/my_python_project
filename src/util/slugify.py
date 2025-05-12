#!/usr/bin/env python3
"""
File: slugify.py
Description: Provides a function to convert strings into URL-friendly slugs.
Author: You <you@example.com>
Version: 1.0.0
"""

import re


def slugify(text: str) -> str:
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)
    # Remove non-alphanumeric characters except hyphens
    text = re.sub(r"[^a-z0-9-]", "", text)
    # Remove leading and trailing hyphens
    return text.strip("-")
