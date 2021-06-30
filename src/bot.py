import asyncio
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
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

responses = ["SHUT UP JOSH!!!!!!", "YO MAMA!!!!!!", "NICE ONE!!!!!!", "SO MEAN!!!!!!", "THAT'S RESPECT!!!!!!"]
phrases = ['mama', 'mom', 'mother']


@client.event
async def on_message(message):
    if message.content[0:2] == '!p' or message.content[0:2] == '-p':
        for s in phrases:
            if s in message.content.lower():
                await message.reply('STOP PLAYING YO MAMA JOKES!!!!!!')
                await asyncio.sleep(1)
                for members in message.author.voice.channel.members:
                    if members.id == 235088799074484224 or members.id == 234395307759108106:
                        await members.edit(voice_channel=None)
                        return
    if message.author.id != 404383046733791233:
        return
    else:
        rand = random.random() * 100
        if rand > 92:
            await message.reply(file=discord.File('C:/Users/crayo/Anti_Troll_Discord_Bot/facebank.jpg'))
        elif rand > 65:
            await message.reply(responses[random.randrange(0, len(responses))])

client.run(TOKEN)
