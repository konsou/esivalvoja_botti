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

        self.assertIsNotNone(os.getenv('BOT_KILL_COMMAND', default=None),
                             "BOT_KILL_COMMAND must be set")

        required_tokens = {
            'production': ('DISCORD_TOKEN',),
            'development': ('DISCORD_TOKEN_DEVELOPMENT',
                            'DISCORD_TEST_CLIENT_TOKEN'),
        }


        for token_name in required_tokens[environment]:
            self.assertIsNotNone(os.getenv(token_name, default=None),
                                 f"must have a discord token set for {environment}: {token_name}")
            self.assertTrue(len(os.getenv(token_name).strip()) == 59,
                            f"discord token {token_name} must be 59 characters long")


