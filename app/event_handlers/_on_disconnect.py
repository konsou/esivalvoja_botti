import discord


async def on_disconnect(client: discord.Client):
    print(f"Disconnected")