import os
import json
from collections import defaultdict
from time import time
from random import choice

import discord
from dotenv import load_dotenv

from app.options import Options
from app.response import load_responses, get_response
from app.triggers import load_triggers, is_activated
from app.services import daily_text
from app.funnify_text import funnify_text


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

    with open('app/json_data/string_replacements.json', encoding='utf8') as f:
        funnify_text_replacements = json.load(f)

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

        if not message.guild:  # is a DM
            if os.getenv('BOT_KILL_COMMAND') in message.content:
                await message.author.send('valid kill command - disconnecting')
                await client.close()
            return

        if client.user in message.mentions:  # done this way to NOT respond to @everyone and @here
            msg_lower = message.content.lower()
            activated_trigger = is_activated(msg_lower, triggers)
            if activated_trigger is None:
                # no valid trigger words
                print(message.content)
                reply_msg = f"{choice(responses['dont_understand'])} {message.author.mention}"
                print(reply_msg)
                await message.channel.send(reply_msg)
            elif activated_trigger == 'regret':
                print(message.content)
                reply_msg = get_response(user_name=message.author.name,
                                         last_regret_timestamp=last_regrets_timestamps[message.author.id],
                                         options=options,
                                         responses=responses)
                reply_msg = f"{reply_msg} {message.author.mention}"
                last_regrets_timestamps[message.author.id] = time()
                print(reply_msg)
                await message.channel.send(reply_msg)
            elif activated_trigger == 'daily_text':
                if not daily_text.result_is_cached():
                    await message.channel.send(f"Hetkinen vain, kaivan päiväntekstikirjasen hyllystä...")

                text = await daily_text.daily_text()
                text = funnify_text(text=text,
                                    text_replacements=funnify_text_replacements,
                                    options=options)
                reply_msg = f"Tässäpä sinulle tämän päivän teksti {message.author.mention}:\n\n{text} "
                print(reply_msg)
                await message.channel.send(reply_msg)

    client.run(TOKEN)


if __name__ == '__main__':
    print(f"Don't run this file as a script. Use the main.py in the project top folder.")
