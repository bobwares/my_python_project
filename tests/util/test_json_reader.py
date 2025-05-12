"""
File: tests/util/test_json_reader.py
Description: Unit test for util.json_reader.read_json_file.
Author: bobwares codebot
"""

import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from util.json_reader import read_json_file


class TestJsonReader(unittest.TestCase):
    def test_read_valid_json_file(self):
        with TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "sample.json"
            sample_data = {"name": "bobwares", "language": "Python"}

            with open(test_path, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f)

            result = read_json_file(test_path)

            self.assertIsInstance(result, dict)
            self.assertEqual(result["name"], "bobwares")
            self.assertEqual(result["language"], "Python")

    def test_read_invalid_json_file(self):
        with TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "corrupt.json"
            test_path.write_text('{"incomplete_json": true', encoding='utf-8')

            with self.assertRaises(json.JSONDecodeError):
                read_json_file(test_path)


if __name__ == "__main__":
    unittest.main()
