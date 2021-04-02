import unittest
import os
from dotenv import load_dotenv

load_dotenv()


class TestEnvironment(unittest.TestCase):
    def test_environment_ok(self):
        """
        Test that the environment is correctly set
        """
        environment = os.getenv('ENVIRONMENT')

        self.assertTrue(any(s == environment for s in ('production', 'development')),
                        "ENVIRONMENT must be 'production' or 'development'")

        token_key_names = {
            'production': 'DISCORD_TOKEN',
            'development': 'DISCORD_TOKEN_DEVELOPMENT',
        }
        required_key_name = token_key_names[environment]
        self.assertIsNotNone(os.getenv(required_key_name, default=None),
                             f"must have a discord token set for {environment}: {required_key_name}")
        self.assertTrue(len(os.getenv(required_key_name).strip()) == 59,
                        f"discord token must be 59 characters long")


