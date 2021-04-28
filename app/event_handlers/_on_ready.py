import discord


async def on_ready(client: discord.Client):
    print(f'{client.user} has connected to Discord!')