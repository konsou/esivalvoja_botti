import os
from collections import defaultdict
from time import time
from random import choice

import discord
from dotenv import load_dotenv

from app.options import Options
from app.response import load_responses, get_response
from app.triggers import load_triggers, is_activated


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
    options = Options('app/options.json')
    responses = load_responses('app/json_data/responses.json')
    triggers = load_triggers('app/json_data/triggers.json')

    # key: user id, value: timestamp of last regret
    last_regrets_timestamps: defaultdict[int, float] = defaultdict(lambda: 0)  # default value: 0

    client = discord.Client()
    print(f"Bot starting...")

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_disconnect():
        print(f"Disconnected")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.lower() == "ping?":
            await message.channel.send("pong!")
            return

        if not message.guild:  # is a DM
            if os.getenv('BOT_KILL_COMMAND') in message.content:
                await message.author.send('valid kill command')
                await client.close()
            return

        if client.user in message.mentions:  # done this way to NOT respond to @everyone and @here
            msg_lower = message.content.lower()
            if is_activated(msg_lower, triggers):
                print(message.content)
                reply_msg = get_response(user_name=message.author.name,
                                         last_regret_timestamp=last_regrets_timestamps[message.author.id],
                                         options=options,
                                         responses=responses)
                reply_msg = f"{reply_msg} {message.author.mention}"
                last_regrets_timestamps[message.author.id] = time()
                print(reply_msg)

                await message.channel.send(reply_msg)
            else:  # no valid trigger words
                print(message.content)
                reply_msg = f"{choice(responses['dont_understand'])} {message.author.mention}"
                print(reply_msg)
                await message.channel.send(reply_msg)

    client.run(TOKEN)


if __name__ == '__main__':
    print(f"Don't run this file as a script. Use the main.py in the project top folder.")
