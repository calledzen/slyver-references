import random
import os
import discord
import asyncio
from dotenv import load_dotenv
from utils.monitoring import monitoring
from utils.database import connect, disconnect, tableSetup

load_dotenv()
bot = discord.Bot(intents=discord.Intents.all(), debug_guilds=[990724201105227898])




@bot.event
async def on_ready():
    print("-----------")
    print("bot system loaded.")
    print("name: " + bot.user.name)
    print("-----------")
    connect("mariadb")
    tableSetup()





print("COMMANDS")
for filename in os.listdir('commands'):
    if filename.endswith('.py'):
        if filename != "__init__.py":
            bot.load_extension(f'commands.{filename[:-3]}')
            print(f'[+] {filename[:-3]}')
print("EVENTS")
for filename in os.listdir('events'):
    if filename.endswith('.py'):
        if filename != "__init__.py":
            bot.load_extension(f'events.{filename[:-3]}')
            print(f'[+] {filename[:-3]}')



async def change_presence_task():
    await bot.wait_until_ready()
    _guild = bot.get_guild(int(os.getenv('GUILD_ID')))
    e = random.choice(_guild.members)
    while e.bot:
        e = random.choice(_guild.members)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                        name=f"{random.choice(['❤️','🧡','💛','💚','💙','💜','🖤','🤍','🤎'])}┃mit {e.display_name}"))
    await asyncio.sleep(20)


bot.loop.create_task(change_presence_task())



monitoring()
bot.run(str(os.getenv('TOKEN')))

