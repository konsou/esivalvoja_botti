from __future__ import annotations
import os
import json
from collections import defaultdict
from time import time
from random import choice
from dataclasses import dataclass
from typing import TYPE_CHECKING

import discord
from dotenv import load_dotenv

from app.options import Options
from app.response import load_responses, get_response
from app.triggers import load_triggers, is_activated
from app.services import daily_text
from app.funnify_text import load_text_replacements, funnify_text

if TYPE_CHECKING:
    from app.response import AllResponses
    from app.triggers import AllTriggers
    from app.funnify_text import TextReplacements

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT')

if ENVIRONMENT == 'development':
    TOKEN = os.getenv('DISCORD_TOKEN_DEVELOPMENT')
elif ENVIRONMENT == 'production':
    TOKEN = os.getenv('DISCORD_TOKEN')
else:
    raise ValueError(f"Invalid ENVIRONMENT value - must be 'development' or 'production', was '{ENVIRONMENT}'")
print(f"ENVIRONMENT: {ENVIRONMENT}")


@dataclass
class AppData:
    responses: AllResponses
    triggers: AllTriggers
    funnify_text_replacements: TextReplacements


def main():
    options = Options('app/options.json')
    _responses = load_responses('app/json_data/responses.json')
    _triggers = load_triggers('app/json_data/triggers.json')
    _funnify_text_replacements = load_text_replacements(options.funnify_text_replacement_file,
                                                        options=options)
    data = AppData(responses=_responses,
                   triggers=_triggers,
                   funnify_text_replacements=_funnify_text_replacements)

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
            activated_trigger = is_activated(msg_lower, data.triggers)
            if activated_trigger is None:
                # no valid trigger words
                print(message.content)
                reply_msg = f"{choice(data.responses['dont_understand'])} {message.author.mention}"
                print(reply_msg)
                await message.channel.send(reply_msg)
            elif activated_trigger == 'regret':
                print(message.content)
                reply_msg = get_response(user_name=message.author.name,
                                         last_regret_timestamp=last_regrets_timestamps[message.author.id],
                                         options=options,
                                         responses=data.responses)
                reply_msg = f"{reply_msg} {message.author.mention}"
                last_regrets_timestamps[message.author.id] = time()
                print(reply_msg)
                await message.channel.send(reply_msg)
            elif activated_trigger == 'daily_text':
                if not daily_text.result_is_cached():
                    await message.channel.send(f"Hetkinen vain, kaivan päiväntekstikirjasen hyllystä...")

                text = await daily_text.daily_text()

                if options.watch_json_data_files:
                    _new_replacements = load_text_replacements(options.funnify_text_replacement_file,
                                                               options=options)
                    if _new_replacements['__hash__'][0] != data.funnify_text_replacements['__hash__'][0]:
                        print(f"Reloading text replacements")
                        data.funnify_text_replacements = _new_replacements

                text = funnify_text(text=text,
                                    text_replacements=data.funnify_text_replacements,
                                    options=options)
                reply_msg = f"Tässäpä sinulle tämän päivän teksti {message.author.mention}:\n\n{text} "
                print(reply_msg)
                await message.channel.send(reply_msg)

    client.run(TOKEN)


if __name__ == '__main__':
    print(f"Don't run this file as a script. Use the main.py in the project top folder.")
