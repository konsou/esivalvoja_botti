# HERE'S A WORKING COMMAND:
# python .\example_tester.py 825623768763596801 ODI3NTkxMzEyNTYzODk2Mzgw.YGdQeA.NRNK0xmVzmaJNXnMDgLVp8fL5-M -c 688775528831910000 -r all
import unittest
import os
import time
import asyncio

import discord
from dotenv import load_dotenv

# load_dotenv()

'''
class TestTriggers(unittest.TestCase):
    def test_can_join_server(self):
        """
        Test that the bot can connect to Discord
        """

        token = os.getenv('DISCORD_TOKEN_DEVELOPMENT')

        client = discord.Client()

        # THIS WORKS OTHERWISE BUT THROWS AN "Event loop is closed" RuntimeError AFTER EXIT

        @client.event
        async def on_ready():
            print(f'{client.user} has connected to Discord!')
            await print_loop()
            await client.close()
            # await asyncio.sleep(5)
            await print_loop()
            # return True

        @client.event
        async def on_error(err):
            print(f'Error connecting to Discord: {err}')
            # return False

        async def print_loop():
            print(f"loop is {asyncio.get_running_loop()}")


        client.run(token)
        time.sleep(5)
        print("after")
        print(f"client closed: {client.is_closed()}")

'''
