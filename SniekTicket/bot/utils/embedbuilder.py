import asyncio
import discord
from datetime import datetime



def buildEmbed(title, text, color = None, emojiu = None):
    coloru = discord.Color.embed_background() if color == None else color
    if emojiu != None:
        e = discord.Embed(title=f"`{emojiu}` ┃ " + title, colour=coloru, description=text, timestamp=datetime.utcnow())
        e.set_footer(text="Sniek Ticket",
                         icon_url="https://cdn.discordapp.com/app-icons/990726420932227154/d5829221e531b3fc4b3d97cf65428c6c.png?size=1024")
        return e
    else:
        e = discord.Embed(title=title, colour=coloru, description=text, timestamp=datetime.utcnow())
        e.set_footer(text="Sniek Ticket",
                         icon_url="https://cdn.discordapp.com/app-icons/990726420932227154/d5829221e531b3fc4b3d97cf65428c6c.png?size=1024")
        return e




def buildErrorMessage(text):
    e = discord.Embed(title="`❌` ┃ Error", colour=0xF44F4F, description=f"_{text}_", timestamp=datetime.utcnow())
    e.set_footer(text="Sniek Ticket",
                 icon_url="https://cdn.discordapp.com/app-icons/990726420932227154/d5829221e531b3fc4b3d97cf65428c6c.png?size=1024")
    return e


async def sendErrorMessage(ctx, text):
    e = discord.Embed(title="`❌` ┃ Error", colour=0xF44F4F, description=f"_{text}_", timestamp=datetime.utcnow())
    e.set_footer(text="Sniek Ticket",
                         icon_url="https://cdn.discordapp.com/app-icons/990726420932227154/d5829221e531b3fc4b3d97cf65428c6c.png?size=1024")
    errmsg = await ctx.reply(embed=e)
    await asyncio.sleep(7)
    await errmsg.delete()
