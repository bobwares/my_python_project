"""
File: src/util/json_reader.py
Description: Utility for reading JSON files.
Author: bobwares codebot
"""

import json
from pathlib import Path
from typing import Any
import importlib.resources

def read_json_file(file_path: Path) -> dict[str, Any]:
    """
    Reads a JSON file and returns its contents as a dictionary.

    Args:
        file_path (Path): Path to the JSON file.

    Returns:
        dict: Parsed JSON content.
    """
    with importlib.resources.files("my_package.resources").joinpath("prompts.json").open("r", encoding="utf-8") as f:
        return json.load(f)
