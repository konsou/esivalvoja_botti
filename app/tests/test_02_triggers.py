import unittest

from app.triggers import load_triggers, is_activated


class TestTriggers(unittest.TestCase):
    def test_has_contents(self):
        """
        Test that triggers has correct contents
        """
        triggers = load_triggers('app/json_data/triggers.json')
        self.assertIsInstance(triggers, dict, 'triggers is a dictionary')
        for trigger_key in ('regret', 'daily_text', 'opinion'):
            self.assertIn(trigger_key, triggers.keys(), f'triggers has a key "{trigger_key}"')
            self.assertIn('partial', triggers[trigger_key], f'{trigger_key} triggers has a key "partial"')
            self.assertTrue(len(triggers[trigger_key]['partial']),
                            f'{trigger_key} partial word triggers length more than 0')

    def test_trigger_regret(self):
        """
        Test "regret" trigger activation
        """
        all_triggers = load_triggers('app/json_data/triggers.json')
        regret_triggers = all_triggers['regret']
        test_triggers_positive = (regret_triggers['partial'][0],
                                  "kaduttaa",
                                  "kyllä nyt iski katumus :(",
                                  )
        test_triggers_negative = ("well this shouldn't activate",
                                  f"{regret_triggers['partial'][0][:-1]}!!",
                                  )
        for t in test_triggers_positive:
            self.assertEqual('regret', is_activated(message=t, triggers=all_triggers),
                             f"trigger should activate: \"{t}\"")

        for t in test_triggers_negative:
            self.assertIsNone(is_activated(message=t, triggers=all_triggers),
                              f"trigger shouldn't activate: \"{t}\"")

    def test_trigger_daily_text(self):
        """
        Test "daily_text" trigger activation
        """
        all_triggers = load_triggers('app/json_data/triggers.json')
        daily_text_triggers = all_triggers['daily_text']
        test_triggers_positive = (daily_text_triggers['partial'][0],
                                  "annapas botti meille päivän sana!",
                                  "päivänteksti olisi kyllä poikaa",
                                  )
        test_triggers_negative = ("well this shouldn't activate",
                                  f"{daily_text_triggers['partial'][0][:-1]}!!",
                                  )
        for t in test_triggers_positive:
            self.assertEqual('daily_text', is_activated(message=t, triggers=all_triggers),
                             f"trigger should activate: \"{t}\"")

        for t in test_triggers_negative:
            self.assertIsNone(is_activated(message=t, triggers=all_triggers),
                              f"trigger shouldn't activate: \"{t}\"")

    def test_trigger_opinion(self):
        """
        Test "opinion" trigger activation
        """
        opinions = load_triggers('app/json_data/triggers.json')
        opinions_triggers = opinions['opinion']
        test_triggers_positive = (opinions_triggers['partial'][0],
                                  "Mikäs on mielipiteesi käyttäjästä (joku)",
                                  "mielipide errki?",
                                  )
        test_triggers_negative = ("well this shouldn't activate",
                                  f"{opinions_triggers['partial'][0][:-1]}!!",
                                  )
        for t in test_triggers_positive:
            self.assertEqual('opinion', is_activated(message=t, triggers=opinions),
                             f"trigger should activate: \"{t}\"")

        for t in test_triggers_negative:
            self.assertIsNone(is_activated(message=t, triggers=opinions),
                              f"trigger shouldn't activate: \"{t}\"")


