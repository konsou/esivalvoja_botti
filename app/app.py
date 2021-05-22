from __future__ import annotations
import os
from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING

import discord
from dotenv import load_dotenv

from app.options import Options
from app.response import load_responses
from app.triggers import load_triggers
from app.funnify_text import load_text_replacements
from app.opinion import load_opinions
from app import event_handlers

if TYPE_CHECKING:
    from app.response import AllResponses
    from app.triggers import AllTriggers
    from app.funnify_text import TextReplacements
    from app.opinion import Opinions

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
    opinions: Opinions
    # key: user id, value: timestamp of last regret
    last_regrets_timestamps: defaultdict[int, float]


def main():
    options = Options('app/options.json')
    _responses = load_responses('app/json_data/responses.json')
    _triggers = load_triggers('app/json_data/triggers.json')
    _funnify_text_replacements = load_text_replacements(options.funnify_text_replacement_file,
                                                        options=options)
    _opinions = load_opinions('app/json_data/opinions.json')
    app_data = AppData(responses=_responses,
                       triggers=_triggers,
                       funnify_text_replacements=_funnify_text_replacements,
                       opinions=_opinions,
                       last_regrets_timestamps=defaultdict(lambda: 0))  # default value: 0

    client = discord.Client()
    print(f"Bot starting...")

    @client.event
    async def on_ready():
        await event_handlers.on_ready(client)

    @client.event
    async def on_disconnect():
        await event_handlers.on_disconnect(client)

    @client.event
    async def on_message(message):
        await event_handlers.on_message(message,
                                        client=client,
                                        app_data=app_data,
                                        options=options)

    client.run(TOKEN)


if __name__ == '__main__':
    print(f"Don't run this file as a script. Use the main.py in the project top folder.")
