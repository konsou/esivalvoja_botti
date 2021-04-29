from __future__ import annotations
import os
from random import choice
from time import time
from typing import TYPE_CHECKING

import discord

from app.response import get_response
from app.triggers import is_activated
from app.services import daily_text
from app.funnify_text import load_text_replacements, funnify_text

if TYPE_CHECKING:
    from app.app import AppData
    from app.options import Options


async def on_message(message: discord.Message,
                     client: discord.Client,
                     app_data: AppData,
                     options: Options):
    if message.author == client.user:
        return

    if not message.guild:  # is a DM
        if os.getenv('BOT_KILL_COMMAND') in message.content:
            await message.author.send('valid kill command - disconnecting')
            await client.close()
        return

    if client.user in message.mentions:  # done this way to NOT respond to @everyone and @here
        msg_lower = message.content.lower()
        activated_trigger = is_activated(msg_lower, app_data.triggers)
        if activated_trigger is None:
            # no valid trigger words
            print(message.content)
            reply_msg = f"{choice(app_data.responses['dont_understand'])} {message.author.mention}"
            print(reply_msg)
            await message.channel.send(reply_msg)
        elif activated_trigger == 'regret':
            print(message.content)
            reply_msg = get_response(user_name=message.author.name,
                                     last_regret_timestamp=app_data.last_regrets_timestamps[message.author.id],
                                     options=options,
                                     responses=app_data.responses)
            reply_msg = f"{reply_msg} {message.author.mention}"
            app_data.last_regrets_timestamps[message.author.id] = time()
            print(reply_msg)
            await message.channel.send(reply_msg)
        elif activated_trigger == 'daily_text':
            if not daily_text.result_is_cached():
                await message.channel.send(f"Hetkinen vain, kaivan päiväntekstikirjasen hyllystä...")

            text = await daily_text.daily_text(timezone=options.timezone)

            if options.watch_json_data_files:
                _new_replacements = load_text_replacements(options.funnify_text_replacement_file,
                                                           options=options)
                if _new_replacements['__hash__'][0] != app_data.funnify_text_replacements['__hash__'][0]:
                    print(f"Reloading text replacements")
                    app_data.funnify_text_replacements = _new_replacements

            text = funnify_text(text=text,
                                text_replacements=app_data.funnify_text_replacements,
                                options=options)
            reply_msg = f"Tässäpä sinulle tämän päivän teksti {message.author.mention}:\n\n{text} "
            print(reply_msg)
            await message.channel.send(reply_msg)
