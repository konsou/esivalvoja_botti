import os
import json
import discord

from dotenv import load_dotenv
from app.reaction import get_reaction
from collections import defaultdict
from time import time

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT')

if ENVIRONMENT == 'development':
    TOKEN = os.getenv('DISCORD_TOKEN_DEVELOPMENT')
elif ENVIRONMENT == 'production':
    TOKEN = os.getenv('DISCORD_TOKEN')
else:
    raise ValueError(f"Invalid ENVIRONMENT value - must be 'development' or 'production', was '{ENVIRONMENT}'")
print(f"ENVIRONMENT: {ENVIRONMENT}")


def main():
    client = discord.Client()

    print(f"Bot starting...")

    with open('json_data/triggers.json', encoding='utf-8') as f:
        trigger_words = json.load(f)['partial']
        print(f"Trigger words loaded")

    # key: user id, value: timestamp of last regret
    last_regrets_timestamps: defaultdict[int, float] = defaultdict(lambda: 0)  # default value: 0

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        msg_lower = message.content.lower()
        if any((word in msg_lower for word in trigger_words)):
            print(message.content)
            reply_msg = get_reaction(message.author.name, last_regrets_timestamps[message.author.id])
            reply_msg = f"{reply_msg} {message.author.mention}"
            last_regrets_timestamps[message.author.id] = time()
            print(reply_msg)

            await message.channel.send(reply_msg)

    client.run(TOKEN)


if __name__ == '__main__':
    main()
