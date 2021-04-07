import unittest
import os
import time
import asyncio

import discord
from dotenv import load_dotenv

load_dotenv()


class TestDiscordIntegration(unittest.TestCase):
    def test_can_join_server(self):
        """
        Test that the bot can connect to Discord
        """

        token = os.getenv('DISCORD_TOKEN_DEVELOPMENT')

        client = discord.Client()

        # THIS WORKS OTHERWISE BUT THROWS AN "Event loop is closed" RuntimeError AFTER EXIT
        # May be a Windows bug?

        @client.event
        async def on_ready():
            await client.close()
            return True

        @client.event
        async def on_error(err):
            raise

        client.run(token)
        print("after")
        print(f"client closed: {client.is_closed()}")

