import unittest
import datetime

from app.opinion import load_opinions, get_opinion, Opinions


class TestOpinion(unittest.TestCase):
    def test_has_contents(self):
        """
        Test that opinions has contents
        """
        opinions = load_opinions('app/json_data/opinions.json')
        self.assertTrue(len(opinions), 'opinions has a length of more than 0')
        self.assertIsInstance(opinions, dict, 'opinions type is correct')

    def test_opinion(self):
        """
        Test opinion functionality
        """
        opinions = load_opinions('app/json_data/opinions.json')

        no_opinion = "Ei minulla hänestä oikein sen ihmeempää mielipidettä ole."
        konso_opinion = "Jokainen rakennus on tietenkin jonkun rakentama, mutta Esivalvojan rakentaja on konso."

        self.assertEqual(get_opinion(user_name='asdlfjh33kjshafdlkjh-NOT-EXISTING-USER-NAME',
                                     opinions=opinions),
                         no_opinion,
                         "no opinion should activate for unknown user")

        self.assertEqual(get_opinion(user_name='konso',
                                     opinions=opinions),
                         konso_opinion,
                         f"konso opinion should be \"{konso_opinion}\"")



