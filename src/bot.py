import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

responses = ["SHUT UP JOSH!!!!!!", "YO MAMA", "nice one", "so mean", "334-202-0003"]


@client.event
async def on_message(message):
    if message.author.id != 403745233507975169:
        return
    else:
        if random() * 100 > 69:
            await message.reply(responses[random.randrange(0, responses.len)])

client.run(TOKEN)
