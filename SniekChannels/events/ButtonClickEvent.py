import asyncio
import datetime
import os
import time

import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.embedbuilder import buildEmbed, buildErrorMessage
import discord.ui as ui
import utils.database as db
import discord.utils
from dateutil import tz
from threading import Thread


class ChangeNameModal(ui.Modal):

    def __init__(self) -> None:

        super().__init__(title="Channel Namen ändern")
        self.add_item(ui.InputText(label="Channel Namen", placeholder="Schreibe hier den neuen Channel Namen rein", required=True, style=discord.InputTextStyle.short, max_length=75))

    async def callback(self, interaction: discord.Interaction):
        await interaction.user.voice.channel.edit(name="『🔊』" + self.children[0].value)
        await interaction.response.send_message(
            embed=buildEmbed(title="AutoChannel System", text="Der Channel Name wurde geändert!", color=0x76FF84),
            ephemeral=True)


class ChangeLimitCustom(ui.Modal):

    def __init__(self) -> None:

        super().__init__(title="User Limit ändern")
        self.add_item(ui.InputText(label="User Limit ändern", placeholder="Schreibe hier das User Limit für deinen Channel rein", required=True, style=discord.InputTextStyle.short, max_length=2, min_length=1 ))

    async def callback(self, interaction: discord.Interaction):
        _userlimit = self.children[0].value
        if _userlimit.isnumeric() and int(_userlimit) >= 0:
            await interaction.user.voice.channel.edit(user_limit=int(_userlimit))
            await interaction.response.send_message(
                embed=buildEmbed(title="AutoChannel System", text="Das Userlimit wurde geändert", color=0x76FF84),
                ephemeral=True)
        else:
            await interaction.response.send_message(
                embed=buildErrorMessage(text="Du musst eine Zahl zwischen 0 und 99 angeben", color=0x76FF84),
                ephemeral=True)




class ButtonClickEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.userblockedname = []
    @commands.Cog.listener()
    async def on_interaction(self, interaction):


        if interaction.custom_id == "channelinfo":

            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return

            banneduserstr = ""
            if(db.checkData("banneduser", "channelid=" + str(interaction.user.voice.channel.id))):
                for userid in db.convertData(
                        db.getData("banneduser", "userid", f"channelid='{interaction.user.voice.channel.id}'"),
                        "list"):
                    banneduserstr += f"<@{userid}>, "



            else:
                banneduserstr = "Keine"
            e = discord.Embed(title="Informationen", description="Hier siehst du alle wichtigen Informationen zu deinem aktuellen Channel", color=discord.Color.embed_background())
            e.add_field(name="Name", value=str(interaction.user.voice.channel.name), inline=False)
            e.add_field(name="ID", value=str(interaction.user.voice.channel.id),
                        inline=False)
            e.add_field(name="Owner", value=interaction.guild.get_member(db.convertData(db.getData("channels", "ownerid", "channelid='" + str(interaction.user.voice.channel.id) + "'"), "int")).name + "#" + interaction.guild.get_member(db.convertData(db.getData("channels", "ownerid", "channelid='" + str(interaction.user.voice.channel.id) + "'"), "int")).discriminator, inline=False)
            e.add_field(name="Erstellt", value=str(interaction.user.voice.channel.created_at.astimezone(tz.gettz('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')), inline=False)
            e.add_field(name="Mitglieder", value=str(len(interaction.user.voice.channel.voice_states.keys())) if interaction.user.voice.channel.user_limit == 0 else str(len(interaction.user.voice.channel.voice_states.keys())) + "/" + str(interaction.user.voice.channel.user_limit), inline=False)
            e.add_field(name="Gebannte User", value=banneduserstr,
                        inline=False)


            await interaction.response.send_message(embed=e, ephemeral=True)



        #---------------------------------------------------------------------------------------------------------------------- CHANGE VISIBILITY



        elif interaction.custom_id == "changevisibility_off":

            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return

            if str(interaction.user.voice.channel.id) in db.convertData(db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):
                await interaction.user.voice.channel.set_permissions(interaction.user.voice.channel.guild.default_role, view_channel=False)
                await interaction.user.voice.channel.set_permissions(interaction.user.voice.channel.guild.get_role(
                    db.convertData(
                        db.getData("settings", "teamid", f"categoryid = '{interaction.user.voice.channel.category.id}'")[0],
                        "int")), view_channel=True)
                await interaction.response.send_message(embed=buildEmbed(title="AutoChannel System", text="Dein Channel ist nun vor allen versteckt!", color=0xFF7676), ephemeral=True)
            else:
                await interaction.response.send_message(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                        ephemeral=True)
        elif interaction.custom_id == "changevisibility_on":

            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return

            if str(interaction.user.voice.channel.id) in db.convertData(db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):
                await interaction.user.voice.channel.set_permissions(interaction.user.voice.channel.guild.default_role, view_channel=True)
                await interaction.user.voice.channel.set_permissions(interaction.user.voice.channel.guild.get_role(
                    db.convertData(
                        db.getData("settings", "teamid", f"categoryid = '{interaction.user.voice.channel.category.id}'")[0],
                        "int")), view_channel=True)
                await interaction.response.send_message(embed=buildEmbed(title="AutoChannel System", text="Dein Channel ist nun nicht mehr vor allen versteckt", color=0x76FF84), ephemeral=True)
            else:
                await interaction.response.send_message(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                    ephemeral=True)
        #---------------------------------------------------------------------------------------------------------------------- CHANGE LOCK MODE


        elif interaction.custom_id == "changelockmode_on":

            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return

            if str(interaction.user.voice.channel.id) in db.convertData(db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):
                await interaction.user.voice.channel.set_permissions(interaction.user.voice.channel.guild.default_role, connect=False)
                await interaction.user.voice.channel.set_permissions(interaction.user.voice.channel.guild.get_role(
                    db.convertData(
                        db.getData("settings", "teamid", f"categoryid = '{interaction.user.voice.channel.category.id}'")[0],
                        "int")), connect=True)
                await interaction.response.send_message(embed=buildEmbed(title="AutoChannel System", text="Dein Channel kann nun von keinem mehr betreten werden!", color=0x76FF84), ephemeral=True)
            else:
                await interaction.response.send_message(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                    ephemeral=True)
        elif interaction.custom_id == "changelockmode_off":

            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return

            if str(interaction.user.voice.channel.id) in db.convertData(db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):
                await interaction.user.voice.channel.set_permissions(interaction.user.voice.channel.guild.default_role, connect=True)
                await interaction.user.voice.channel.set_permissions(interaction.user.voice.channel.guild.get_role(
                    db.convertData(
                        db.getData("settings", "teamid", f"categoryid = '{interaction.user.voice.channel.category.id}'")[0],
                        "int")), connect=True)



                await interaction.response.send_message(embed=buildEmbed(title="AutoChannel System", text="Dein Channel kann nun von jedem betreten werden!", color=0xFF7676), ephemeral=True)
            else:
                await interaction.response.send_message(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                    ephemeral=True)

        #---------------------------------------------------------------------------------------------------------------------- CHANGE USERLIMIT
        elif interaction.custom_id == "changeuserlimit_plus1":

            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return


            if str(interaction.user.voice.channel.id) in db.convertData(db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):
                await interaction.user.voice.channel.edit(user_limit=interaction.user.voice.channel.user_limit + 1 if interaction.user.voice.channel.user_limit <= 98 else 99)
                await interaction.response.defer()

            else:
                await interaction.response.send_message(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                    ephemeral=True)


        elif interaction.custom_id == "changeuserlimit_minus1":

            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return

            if str(interaction.user.voice.channel.id) in db.convertData(db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):
                await interaction.user.voice.channel.edit(user_limit=interaction.user.voice.channel.user_limit - 1 if interaction.user.voice.channel.user_limit >= 1 else 0)
                await interaction.response.defer()
            else:
                await interaction.response.send_message(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                    ephemeral=True)

        elif interaction.custom_id == "changeuserlimit_remove":

            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return

            if str(interaction.user.voice.channel.id) in db.convertData(db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):
                await interaction.user.voice.channel.edit(user_limit=0)
                await interaction.response.send_message(embed=buildEmbed(title="AutoChannel System", text="Das Userlimit wurde zurückgesetzt", color=0xFF7676), ephemeral=True)
            else:
                await interaction.response.send_message(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                    ephemeral=True)

        elif interaction.custom_id == "changeuserlimit_custom":

            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return

            if str(interaction.user.voice.channel.id) in db.convertData(
                    db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):
                await interaction.response.send_modal(ChangeLimitCustom())
            else:
                await interaction.response.send_message(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                        ephemeral=True)


        # ---------------------------------------------------------------------------------------------------------------------- CHANGE OWNER
        elif interaction.custom_id == "setowner":
            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return
            if str(interaction.user.voice.channel.id) in db.convertData(
                    db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):

                await interaction.response.send_message(embed=buildEmbed(title="AutoChannel System",
                                                                         text="Bitte makiere den User in diesem Channel oder schreibe seine ID in den Chat"), ephemeral=True)
                _uid = interaction.user.id
                _channelinstance = interaction.message.channel
                def check(m):
                    return m.author.id == _uid and m.channel == _channelinstance
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                except:
                    return await interaction.followup.send(embed=buildErrorMessage("Du hast keine Antwort gegeben"), ephemeral=True)

                if msg.mentions or str(msg.content).isnumeric():

                    _target = msg.mentions[0] if msg.mentions else self.bot.get_user(int(msg.content))
                    if _target == None:
                        await msg.delete()
                        return await interaction.followup.send(
                            embed=buildErrorMessage("Der User konnte nicht gefunden werden"), ephemeral=True)
                    if _target.id == interaction.user.id:
                        await msg.delete()
                        return await interaction.followup.send(
                            embed=buildErrorMessage("Dir gehört der Channel bereits"), ephemeral=True)

                    if _target.id in interaction.user.voice.channel.voice_states.keys():
                        db.updateData("channels", "ownerid='" + str(_target.id) + "'", f"channelid = '{interaction.user.voice.channel.id}'")
                        await msg.delete()
                        await interaction.followup.send(embed=buildEmbed(title="AutoChannel System", text="Du hast den Owner des Channels erfolgreich gewechselt", color=0xFF7676), ephemeral=True)
                        return
                    else:
                        await msg.delete()
                        return await interaction.followup.send(
                            embed=buildErrorMessage("Der User ist nicht in deinem Channel"), ephemeral=True)
                else:
                    await msg.delete()
                    return await interaction.followup.send(
                        embed=buildErrorMessage("Du hast keine Antwort gegeben"), ephemeral=True)
            else:
                await interaction.followup.send(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                        ephemeral=True)


        # ---------------------------------------------------------------------------------------------------------------------- KICK USER

        elif interaction.custom_id == "kick":
            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return
            if str(interaction.user.voice.channel.id) in db.convertData(
                    db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):

                await interaction.response.send_message(embed=buildEmbed(title="AutoChannel System",
                                                                         text="Bitte makiere den User in diesem Channel oder schreibe seine ID in den Chat"), ephemeral=True)
                _uid = interaction.user.id
                _channelinstance = interaction.message.channel
                def check(m):
                    return m.author.id == _uid and m.channel == _channelinstance
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                except:
                    return await interaction.followup.send(embed=buildErrorMessage("Du hast keine Antwort gegeben"), ephemeral=True)

                if msg.mentions or str(msg.content).isnumeric():

                    _target = msg.mentions[0] if msg.mentions else self.bot.get_user(int(msg.content))
                    if _target == None:
                        await msg.delete()
                        return await interaction.followup.send(
                            embed=buildErrorMessage("Der User konnte nicht gefunden werden"), ephemeral=True)
                    if _target.id == interaction.user.id:
                        await msg.delete()
                        return await interaction.followup.send(
                            embed=buildErrorMessage("Du kannst dich nicht selber kicken"), ephemeral=True)

                    if _target.id in interaction.user.voice.channel.voice_states.keys():
                        await _target.move_to(None)
                        await msg.delete()
                        await interaction.followup.send(embed=buildEmbed(title="AutoChannel System", text="Du den User erfolgreich gekickt!", color=0xFF7676), ephemeral=True)
                        return
                    else:
                        await msg.delete()
                        return await interaction.followup.send(
                            embed=buildErrorMessage("Der User ist nicht in deinem Channel"), ephemeral=True)
                else:
                    await msg.delete()
                    return await interaction.followup.send(
                        embed=buildErrorMessage("Du hast keine Antwort gegeben"), ephemeral=True)
            else:
                await interaction.followup.send(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                        ephemeral=True)

        # ---------------------------------------------------------------------------------------------------------------------- BAN USER
        elif interaction.custom_id == "ban":
            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return
            if str(interaction.user.voice.channel.id) in db.convertData(
                    db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):

                await interaction.response.send_message(embed=buildEmbed(title="AutoChannel System",
                                                                         text="Bitte makiere den User in diesem Channel oder schreibe seine ID in den Chat"), ephemeral=True)
                _uid = interaction.user.id
                _channelinstance = interaction.message.channel
                def check(m):
                    return m.author.id == _uid and m.channel == _channelinstance
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                except:
                    return await interaction.followup.send(embed=buildErrorMessage("Du hast keine Antwort gegeben"), ephemeral=True)

                if msg.mentions or str(msg.content).isnumeric():

                    _target = msg.mentions[0] if msg.mentions else self.bot.get_user(int(msg.content))
                    if _target == None:
                        await msg.delete()
                        return await interaction.followup.send(
                            embed=buildErrorMessage("Der User konnte nicht gefunden werden"), ephemeral=True)
                    if _target.id == interaction.user.id:
                        await msg.delete()
                        return await interaction.followup.send(
                            embed=buildErrorMessage("Du kannst dich nicht selber bannen"), ephemeral=True)

                    db.insertData("banneduser", "userid, channelid", f"{_target.id}, {interaction.user.voice.channel.id}")
                    await _target.move_to(None)

                    for userid in db.convertData(
                            db.getData("banneduser", "userid", f"channelid='{interaction.user.voice.channel.id}'"),
                            "list"):
                        await interaction.user.voice.channel.set_permissions(
                            interaction.user.voice.channel.guild.get_member(int(userid)), connect=False)

                    await msg.delete()
                    await interaction.followup.send(embed=buildEmbed(title="AutoChannel System", text="Du den User erfolgreich aus dem Channel gebannt!", color=0xFF7676), ephemeral=True)
                    return

                else:
                    await msg.delete()
                    return await interaction.followup.send(
                        embed=buildErrorMessage("Du hast keine Antwort gegeben"), ephemeral=True)
            else:
                await interaction.followup.send(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                        ephemeral=True)

        # ---------------------------------------------------------------------------------------------------------------------- UNBAN USER
        elif interaction.custom_id == "unban":
            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return
            if str(interaction.user.voice.channel.id) in db.convertData(
                    db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):

                await interaction.response.send_message(embed=buildEmbed(title="AutoChannel System",
                                                                         text="Bitte makiere den User in diesem Channel oder schreibe seine ID in den Chat"), ephemeral=True)
                _uid = interaction.user.id
                _channelinstance = interaction.message.channel
                def check(m):
                    return m.author.id == _uid and m.channel == _channelinstance
                try:
                    msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                except:
                    return await interaction.followup.send(embed=buildErrorMessage("Du hast keine Antwort gegeben"), ephemeral=True)

                if msg.mentions or str(msg.content).isnumeric():

                    _target = msg.mentions[0] if msg.mentions else self.bot.get_user(int(msg.content))
                    if _target == None:
                        await msg.delete()
                        return await interaction.followup.send(
                            embed=buildErrorMessage("Der User konnte nicht gefunden werden"), ephemeral=True)
                    if _target.id == interaction.user.id:
                        await msg.delete()
                        return await interaction.followup.send(
                            embed=buildErrorMessage("Du kannst dich nicht selber entbannen, da du nicht gebannt werden kannst"), ephemeral=True)


                    if(db.checkData("banneduser", "*", f"channelid='{str(interaction.user.voice.channel.id)}' AND userid='{str(_target.id)}'")):

                            db.execute(f"DELETE FROM banneduser WHERE channelid='{str(interaction.user.voice.channel.id)}' AND userid='{str(_target.id)}';")
                            await interaction.user.voice.channel.set_permissions(
                                _target, connect=True)
                            for userid in db.convertData(
                                    db.getData("banneduser", "userid",
                                               f"channelid='{interaction.user.voice.channel.id}'"),
                                    "list"):
                                await interaction.user.voice.channel.set_permissions(
                                    interaction.user.voice.channel.guild.get_member(int(userid)), connect=False)
                            await msg.delete()
                            await interaction.followup.send(embed=buildEmbed(title="AutoChannel System", text="Du den User erfolgreich aus dem Channel entbannt!", color=0xFF7676), ephemeral=True)
                            return
                    else:
                            await msg.delete()
                            return await interaction.followup.send(
                                embed=buildErrorMessage("Der User ist nicht gebannt"), ephemeral=True)

                else:
                    await msg.delete()
                    return await interaction.followup.send(
                        embed=buildErrorMessage("Du hast keine Antwort gegeben"), ephemeral=True)
            else:
                await interaction.followup.send(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                        ephemeral=True)


        #---------------------------------------------------------------------------------------------------------------------- CHANGE NAME
        elif interaction.custom_id == "changechannelname":

            if interaction.user.voice == None:
                await interaction.response.send_message(embed=buildErrorMessage("Du bist in keinem Channel"), ephemeral=True)
                return

            if str(interaction.user.voice.channel.id) in db.convertData(
                    db.getData("channels", "channelid", "ownerid='" + str(interaction.user.id) + "'"), "list"):
                if(interaction.user.id in self.userblockedname):
                    return await interaction.response.send_message(embed=buildErrorMessage("Du kannst den Channel Namen nur alle 5 Minuten ändern"), ephemeral=True)
                await interaction.response.send_modal(ChangeNameModal())
                self.userblockedname.append(interaction.user.id)
                def removeuserfromblockedlist():
                    time.sleep(310)
                    self.userblockedname.remove(interaction.user.id)
                t = Thread(target=removeuserfromblockedlist)
                t.start()

            else:
                await interaction.response.send_message(embed=buildErrorMessage("Dir gehört dieser Channel nicht"),
                                                    ephemeral=True)
def setup(bot):
    bot.add_cog(ButtonClickEvent(bot))