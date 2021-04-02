import unittest
import json

from app.triggers import load_triggers


class TestTriggers(unittest.TestCase):
    def test_has_contents(self):
        """
        Test that triggers has correct contents
        """
        self.triggers = load_triggers('app/json_data/triggers.json')
        self.assertIsInstance(self.triggers, dict, 'triggers is a dictionary')
        self.assertIn('partial', self.triggers, 'triggers has a key "partial"')
        self.assertTrue(len(self.triggers['partial']), 'partial word triggers length more than 0')



