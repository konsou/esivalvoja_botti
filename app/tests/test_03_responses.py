import unittest
import time

from app.options import Options
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

    def test_response(self):
        """
        Test response functionality
        """
        responses = load_responses('app/json_data/responses.json')
        options = Options('app/options.json')

        self.assertIn(get_response(user_name='test_user',
                                   last_regret_timestamp=time.time(),
                                   options=options,
                                   responses=responses),
                      responses['too_soon'],
                      f"too_soon response should activate")

        fake_responses = {
            'positive': ["Test %name% replacement"],
            'negative': ["Test %name% replacement"],
        }

        self.assertIn('test_user',
                      get_response(user_name='test_user',
                                   last_regret_timestamp=0,
                                   options=options,
                                   responses=fake_responses),
                      f"%name% should be replaced with user name")
