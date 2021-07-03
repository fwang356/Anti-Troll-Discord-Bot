import asyncio
import os
import discord
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

bot.most = ''
bot.least = ''
bot.user_msg = {}
bot.user_pic = {}


@bot.event
async def on_ready():
    bot.user_msg = {}
    bot.user_pic = {}
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(f'{bot.user.name} has connected to Discord!')

    for channel in guild.text_channels:
        async for message in channel.history(limit=1000):
            if not message.author.bot:
                ide = message.author.id
                if len(message.attachments) > 0:
                    for ext in pic_ext:
                        if message.attachments[0].filename.endswith(ext):
                            if ide not in bot.user_pic:
                                bot.user_pic.update({ide: 0})
                            bot.user_pic[ide] = bot.user_pic[ide] + 1
                if ide not in bot.user_msg:
                    bot.user_msg.update({ide: 0})
                bot.user_msg[ide] = bot.user_msg[ide] + 1
    most_active = []
    least_active = []
    values = list(bot.user_msg.values())
    keys = list(bot.user_msg.keys())
    original_value = len(values)

    for i in range(min(5, int(len(values) / 2 + 1))):
        msg_sent = max(values)
        position = values.index(msg_sent)
        key = keys[position]
        most_active.append(bot.get_user(key).name + ": " + str(msg_sent))
        bot.most = bot.most + most_active[i] + "\n"
        values.remove(msg_sent)
        keys.remove(key)
        if original_value < 6:
            least_active = most_active
            least_active.reverse()
            bot.least = bot.least + least_active[i] + "\n"
        elif len(values) != 0:
            msg_sent = min(values)
            position = values.index(msg_sent)
            key = keys[position]
            least_active.append(guild.get_member(key).name + ": " + str(msg_sent))
            bot.least = bot.least + least_active[i] + "\n"
            values.remove(msg_sent)
            keys.remove(key)
        else:
            break
    print("Done!")


responses = ["SHUT UP JOSH!!!!!!", "YO MAMA!!!!!!", "NICE ONE!!!!!!", "SO MEAN!!!!!!", "THAT'S RESPECT!!!!!!",
             "I'M SAYIN!!!!!!"]
phrases = ['mama', 'mom', 'mother']
pic_ext = ['.jpg', '.png', '.jpeg']


@bot.command(name='stats')
async def stats(ctx):
    response = discord.Embed(title='Server User Analytics', url='https://i.imgur.com/yZUkeeB.png',
                             description="Returns the most and least recently active users in the server, "
                                         "along with the number of messages sent.", color=0x889ceb)
    response.set_thumbnail(url='https://i.imgur.com/yZUkeeB.png')
    response.add_field(name="Most Active", value=bot.most, inline=True)
    response.add_field(name="Least Active", value=bot.least, inline=True)
    await ctx.send(embed=response)


@bot.command(name='user')
async def user(ctx):
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    username = ctx.message.content[6:]
    dude = None
    for members in guild.members:
        if members.name.lower() == username.lower():
            ide = members.id
            dude = members
    if dude.bot:
        await ctx.send("THAT'S A BOT IDIOT!!!!!!")
        return
    if dude is None:
        await ctx.send("WHO IS " + username.upper() + "??????")
        return
    if dude.nick is None:
        response = discord.Embed(title=dude.name, url='https://i.imgur.com/yZUkeeB.png',
                                 description=dude.name + " (ID: " + str(ide) + ")", color=0x889ceb)
    else:
        response = discord.Embed(title=dude.name, url='https://i.imgur.com/yZUkeeB.png',
                                 description=dude.nick + " (ID: " + str(ide) + ")", color=0x889ceb)
    response.set_thumbnail(url=dude.avatar_url)
    response.add_field(name="Created Account On", value=dude.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"),
                       inline=False)
    response.add_field(name="Joined Server On", value=dude.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"),
                       inline=False)
    response.add_field(name="Total Messages Sent", value=bot.user_msg.get(ide), inline=True)
    response.add_field(name="Pictures Sent", value=bot.user_pic.get(ide), inline=True)
    await ctx.send(embed=response)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if message.content[0:2] == '!p' or message.content[0:2] == '-p':
        for s in phrases:
            if s in message.content.lower():
                await message.reply('STOP PLAYING YO MAMA JOKES!!!!!!')
                await asyncio.sleep(1)
                for members in message.author.voice.channel.members:
                    if members.id == 235088799074484224 or members.id == 234395307759108106:
                        await members.edit(voice_channel=None)
                        return
    rand = random.random() * 100
    if message.author.id == 859519371399790614:
        return
    elif message.author.id == 403745233507975169:
        if len(message.attachments) > 0:
            for ext in pic_ext:
                if message.attachments[0].filename.endswith(ext):
                    await message.reply(file=discord.File('C:/Users/crayo/Anti_Troll_Discord_Bot/assets/josh.jpg'))
                    return
        if rand > 95:
            await message.reply(file=discord.File('C:/Users/crayo/Anti_Troll_Discord_Bot/assets/facebank.jpg'))
        elif rand > 90:
            await message.reply(file=discord.File('C:/Users/crayo/Anti_Troll_Discord_bot/assets/facebank_inverted.jpg'))
        elif rand > 50:
            await message.reply(responses[random.randrange(0, len(responses))])
    else:
        if rand > 95:
            await message.reply(file=discord.File('C:/Users/crayo/Anti_Troll_Discord_Bot/assets/facebank_inverted.jpg'))

bot.run(TOKEN)
