import unittest
import os
import time
import asyncio
import platform

import discord
from dotenv import load_dotenv

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

