import os
import discord
from dotenv import load_dotenv
from reaction import get_reaction
from collections import defaultdict
from typing import Dict
from time import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def main():
    client = discord.Client()

    print(f"Bot starting...")

    # key: user id, value: timestamp of last regret
    last_regrets_timestamps: defaultdict[int, float] = defaultdict(lambda: 0)  # default value: 0

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if 'kadun' in message.content.lower():
            print(message.content)
            reply_msg = get_reaction(message.author.name, last_regrets_timestamps[message.author.id])
            reply_msg = f"{reply_msg} {message.author.mention}"
            last_regrets_timestamps[message.author.id] = time()
            print(reply_msg)

            await message.channel.send(reply_msg)

    client.run(TOKEN)


if __name__ == '__main__':
    main()
