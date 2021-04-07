import unittest

from app.triggers import load_triggers, is_activated


class TestTriggers(unittest.TestCase):
    def test_has_contents(self):
        """
        Test that triggers has correct contents
        """
        triggers = load_triggers('app/json_data/triggers.json')
        self.assertIsInstance(triggers, dict, 'triggers is a dictionary')
        self.assertIn('partial', triggers, 'triggers has a key "partial"')
        self.assertTrue(len(triggers['partial']), 'partial word triggers length more than 0')

    def test_trigger_activation(self):
        """
        Test that triggers activate correctly
        """
        triggers = load_triggers('app/json_data/triggers.json')
        test_triggers_positive = (triggers['partial'][0],
                                  "kaduttaa",
                                  "kyllä nyt iski katumus :(",
                                  )
        test_triggers_negative = ("well this shouldn't activate",
                                  f"{triggers['partial'][0][:-1]}!!",
                                  )
        for t in test_triggers_positive:
            self.assertTrue(is_activated(t, triggers),
                            f"trigger should activate: \"{t}\"")

        for t in test_triggers_negative:
            self.assertFalse(is_activated(t, triggers),
                             f"trigger shouldn't activate: \"{t}\"")



