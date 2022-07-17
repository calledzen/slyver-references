import asyncio
import datetime
import os
import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.embedbuilder import buildEmbed
import discord.ui as ui
from manager.Ticket import Ticket, getCurrentTicketID, getAllOpenTickets
import utils.database as db
import discord.utils
from utils.settingsgetter import getTeamRoleID


class ModFirstMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message):

        if isinstance(message.channel, discord.channel.DMChannel) or message.author.bot:
            return





        opentickets = getAllOpenTickets()
        channelsids = []
        for item in opentickets:
            channelsids.append(int(item[2]))
        if(message.channel.id in channelsids):

            ticketdata = None
            for item in opentickets:
                if(item[2] == str(message.channel.id)):
                    ticketdata = item
                    break

            if not discord.utils.get(message.channel.guild.roles, id=int(getTeamRoleID(str(ticketdata[8])))) in message.author.roles:
                return

            if(ticketdata[4] == "0"):
                db.updateData("tickets", "modid='" + str(message.author.id) + "'", f"ticketid={ticketdata[0]}")
                db.setData("moddata", {"userid": message.author.id, "ticketsdone": "ticketsdone + 1", "lastticketid": str(ticketdata[0])})
                await message.channel.set_permissions(message.author, send_messages=True)
                await message.channel.set_permissions(message.channel.guild.get_role(int(getTeamRoleID(str(ticketdata[8])))), send_messages=False, view_channel=True)

                messagereply = await message.channel.history(limit=1, oldest_first=True).flatten()
                _d = await messagereply[0].reply(embed=buildEmbed(title="Ticket System", text=f"Das Ticket wird nun von <@{str(message.author.id)}> übernommen"))
                await asyncio.sleep(15)
                await _d.delete()

        else:
            return


def setup(bot):
    bot.add_cog(ModFirstMessage(bot))