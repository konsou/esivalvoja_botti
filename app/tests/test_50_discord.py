import unittest
import os
import time
import asyncio
import platform
import subprocess

import discord
from dotenv import load_dotenv
from distest import TestCollector, run_dtest_bot

# THIS FIXES AN "Event loop is closed" RuntimeError AFTER EXIT ON WINDOWS
# The error is a known bug Python/Windows bug:
# https://github.com/Rapptz/discord.py/issues/5209#issuecomment-670161023
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()


class TestDiscordIntegration(unittest.TestCase):
    def test_can_join_server(self):
        """
        Test that the bot can connect to Discord
        """

        token = os.getenv('DISCORD_TOKEN_DEVELOPMENT')

        client = discord.Client()

        @client.event
        async def on_ready():
            await client.close()
            return True

        @client.event
        async def on_error(err):
            raise

        client.run(token)

    def test_discord_functions(self):
        """
        Test that the bot responds as it should
        """

        # TODO: THIS
        tester_client_token = os.getenv('DISCORD_TEST_CLIENT_TOKEN')
        test_channel_id = os.getenv('DISCORD_TEST_CHANNEL_ID')
        tester_client = discord.Client()

        test_collector = TestCollector()

        @test_collector()
        async def test_silence(interface):
            """
            Don't reply if not mentioned
            """
            await interface.send_message("Random comment")
            await interface.ensure_silence()

        # Run the main bot as a non-blocking process
        subprocess.Popen(["python3", "main.py"])
        time.sleep(5)
        run_dtest_bot([os.getenv('DISCORD_DEV_BOT_ID'),
                       os.getenv('DISCORD_TEST_CLIENT_TOKEN'),
                       "-c",
                       os.getenv('DISCORD_TEST_CHANNEL_ID'),
                       "-r",
                       "all"],
                      test_collector)

        # test


