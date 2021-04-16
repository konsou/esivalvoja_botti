import unittest

from app.response import load_responses, get_response


class TestResponses(unittest.TestCase):
    def test_has_contents(self):
        """
        Test that responses has correct contents
        """
        responses = load_responses('app/json_data/responses.json')
        self.assertIsInstance(responses, dict, 'responses is a dictionary')
        for key in ('too_soon', 'negative', 'positive', 'dont_understand'):
            self.assertIn(key, responses.keys(), f'responses must have key "{key}"')

        expected_first_responses = {
            'too_soon': "Eiköhän tämä nyt tullut vähän liian nopeasti. Odottele jonkin aikaa niin katsotaan sitten.",
            'negative': "Et kyllä näytä *oikeasti* katuvan. On sellaista seurausten pahoittelua vain tuo.",
            'positive': "Totta kai saat anteeksi, rakas %name%! Katumuksesi on selvästi aitoa ja "
                        "sinulla on aivan ilmeisesti Jehovan siunaus!",
            'dont_understand': "Nyt en ymmärtänyt sinua. Ymmärrän vain katumusta.",
        }
        for key, value in expected_first_responses.items():
            self.assertTrue(responses[key][0] == value, f"invalid data in responses['{key}'][0] - expected:\n"
                                                        f"\"{value}\"\n"
                                                        f"actual value:\n"
                                                        f"\"{responses[key][0]}\"")
    #
    # def test_trigger_activation(self):
    #     """
    #     Test that triggers activate correctly
    #     """
    #     triggers = load_triggers('app/json_data/triggers.json')
    #     test_triggers_positive = (triggers['partial'][0],
    #                               "kaduttaa",
    #                               "kyllä nyt iski katumus :(",
    #                               )
    #     test_triggers_negative = ("well this shouldn't activate",
    #                               f"{triggers['partial'][0][:-1]}!!",
    #                               )
    #     for t in test_triggers_positive:
    #         self.assertTrue(is_activated(t, triggers),
    #                         f"trigger should activate: \"{t}\"")
    #
    #     for t in test_triggers_negative:
    #         self.assertFalse(is_activated(t, triggers),
    #                          f"trigger shouldn't activate: \"{t}\"")
    #
    #
    #
