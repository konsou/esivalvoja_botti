import unittest
import json


class TestJson(unittest.TestCase):
    def test_load_ok(self):
        """
        Test that JSON files can be loaded without an error
        """
        json_files = ('app/json_data/responses.json',
                      'app/json_data/triggers.json',
                      'app/options.json')
        for json_file in json_files:
            try:
                with open(json_file, encoding='utf-8') as f:
                    _ = json.load(f)
            except Exception as e:
                print(json_file)
                print(e)
                raise


