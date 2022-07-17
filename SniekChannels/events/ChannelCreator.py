import asyncio
import datetime
import os
import random

import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.embedbuilder import buildEmbed, buildErrorMessage
import discord.ui as ui
import utils.database as db
import discord.utils



class ChannelCreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):




        if before.channel is not None:
        # -------------------------------- DELETE CHANNEL --------------------------------
            if (str(before.channel.id) in db.convertData(db.getData("channels", "channelid"), "list") and len(
                    before.channel.voice_states.keys()) <= 0):
                await before.channel.delete()
                db.execute(f"DELETE FROM channels WHERE channelid='{str(before.channel.id)}';")
                return
        # -------------------------------- CHANGE OWNER --------------------------------
            if (db.checkData("channels", "channelid", "ownerid='" + str(member.id) + "'")):

                if str(before.channel.id) in db.convertData(
                        db.getData("channels", "channelid", "ownerid='" + str(member.id) + "'"), "list"):
                    _u = str(random.choice(list(before.channel.voice_states.keys())))
                    db.updateData("channels", "ownerid='" + _u + "'", "channelid='" + str(before.channel.id) + "'")
                    _m = await before.channel.guild.get_channel(db.convertData(
                        db.getData("settings", "settingschannelid", f"categoryid = '{before.channel.category.id}'")[0],
                        "int")).send(content=f"<@{_u}>", embed=buildEmbed(title="AutoChannel System",
                                                                          text=f"Der Channel von <@{str(member.id)}> gehört nun <@{_u}>!",
                                                                          color=0x76FF84))
                    await asyncio.sleep(15)
                    await _m.delete()
                    return

        #-------------------------------- CREATE CHANNEL --------------------------------
        if after.channel is not None:
            if str(after.channel.id) in db.convertData(db.getData("settings", "createchannelid"), "list"):
                _channel = await after.channel.guild.create_voice_channel(f'『🔊』{member.display_name}',
                                                                       category=after.channel.category)
                await _channel.set_permissions(after.channel.guild.default_role, view_channel=True)
                await _channel.set_permissions(after.channel.guild.get_role(
                    db.convertData(
                        db.getData("settings", "teamid", f"createchannelid = '{after.channel.id}'")[0],
                        "int")), view_channel=True)
                await member.move_to(_channel)
                db.insertData("channels", "channelid, ownerid", f"{_channel.id}, {member.id}")
                return




def setup(bot):
    bot.add_cog(ChannelCreator(bot))