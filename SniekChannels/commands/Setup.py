import datetime

import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.embedbuilder import buildEmbed
import discord.ui as ui
import utils.database as db


class ChangeVisibility(ui.View):
    @ui.button(style=discord.ButtonStyle.grey, custom_id="changevisibility_on", emoji="👁️")
    async def changevisibilityon_callback(self, button, interaction):
        await interaction.response.defer()
    @ui.button(style=discord.ButtonStyle.grey, custom_id="changevisibility_off", emoji="<:invisible:992847164369813545>")
    async def changevisibilityoff_callback(self, button, interaction):
        await interaction.response.defer()

class ChangeLockMode(ui.View):
    @ui.button(style=discord.ButtonStyle.grey, custom_id="changelockmode_on", emoji="🔒")
    async def changelockmodeon_callback(self, button, interaction):
        await interaction.response.defer()
    @ui.button(style=discord.ButtonStyle.grey, custom_id="changelockmode_off", emoji="🔓")
    async def changelockmodeoff_callback(self, button, interaction):
        await interaction.response.defer()

class ChangeUserLimit(ui.View):
    @ui.button( style=discord.ButtonStyle.grey, custom_id="changeuserlimit_plus1", emoji="➕")
    async def changeuserlimit_plus1_callback(self, button, interaction):
        await interaction.response.defer()

    @ui.button(style=discord.ButtonStyle.grey, custom_id="changeuserlimit_minus1", emoji="➖")
    async def changeuserlimit_minus1_callback(self, button, interaction):
        await interaction.response.defer()

    @ui.button(style=discord.ButtonStyle.grey, custom_id="changeuserlimit_custom", emoji="⚙️")
    async def changeuserlimit_custom_callback(self, button, interaction):
        await interaction.response.defer()
    @ui.button(style=discord.ButtonStyle.grey, custom_id="changeuserlimit_remove", emoji="🗑")
    async def changeuserlimit_remove_callback(self, button, interaction):
        await interaction.response.defer()


class ManageUsers(ui.View):
    @ui.button(emoji="🪓", style=discord.ButtonStyle.grey, custom_id="kick")
    async def kick_callback(self, button, interaction):
        await interaction.response.defer()

    @ui.button(emoji="🔨", style=discord.ButtonStyle.grey, custom_id="ban")
    async def ban_callback(self, button, interaction):
        await interaction.response.defer()

    @ui.button(emoji="<:unban:992846391791599746>", style=discord.ButtonStyle.grey, custom_id="unban")
    async def unban_callback(self, button, interaction):
        await interaction.response.defer()
    @ui.button(emoji="🔑", style=discord.ButtonStyle.grey, custom_id="setowner")
    async def setowner_callback(self, button, interaction):
        await interaction.response.defer()


class ChangeName(ui.View):
    @ui.button(emoji="🖊️", style=discord.ButtonStyle.grey, custom_id="changechannelname")
    async def changechannelname_callback(self, button, interaction):
        await interaction.response.defer()

class ChannelInfoView(ui.View):
    @ui.button(emoji="🔍", style=discord.ButtonStyle.grey, custom_id="channelinfo")
    async def channelinfoview_callback(self, button, interaction):
        await interaction.response.defer()




class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="setup", description="setup command")
    async def _setup(self, ctx: discord.ApplicationContext, settingschannel: discord.Option(discord.TextChannel, required=True), createchannel: discord.Option(discord.VoiceChannel,  required=True), teamrole: discord.Option(discord.Role,  required=True)):

        if not ctx.author.guild_permissions.administrator:
            return


        db.insertData("settings", "teamid, categoryid, settingschannelid, createchannelid", f"'{teamrole.id}', {settingschannel.category.id}, {settingschannel.id} ,{createchannel.id}")





        await settingschannel.send("""
        _ _ 

        > **AUTOCHANNEL SYSTEM**

        _Mit den Knöpfen unten, kannst du deinen eigenen Channel anpassen_
        _ _
        """)

        await settingschannel.send(content="_ _\n",embed=discord.Embed(color=discord.Color.embed_background()).set_image(url="https://i.imgur.com/nikidOA.png"), view=ChangeVisibility())

        await settingschannel.send(content="_ _\n",embed=discord.Embed(color=discord.Color.embed_background()).set_image(url="https://i.imgur.com/Wysvq1e.png"), view=ChangeLockMode())

        await settingschannel.send(content="_ _\n",embed=discord.Embed(color=discord.Color.embed_background()).set_image(url="https://i.imgur.com/FQ4aAQ2.png"), view=ChangeUserLimit())

        await settingschannel.send(content="_ _\n",embed=discord.Embed(color=discord.Color.embed_background()).set_image(url="https://i.imgur.com/5tIJ0SJ.png"), view=ManageUsers())

        await settingschannel.send(content="_ _\n",embed=discord.Embed(color=discord.Color.embed_background()).set_image(url="https://i.imgur.com/m3MGKzX.png"), view=ChangeName())

        await settingschannel.send(content="_ _\n",embed=discord.Embed(color=discord.Color.embed_background()).set_image(url="https://i.imgur.com/0MI2bTN.png"), view=ChannelInfoView())


        await ctx.respond(embed=buildEmbed(title="Setup", text="Setup erfolgreich abgeschlossen", emojiu="✅"))




def setup(bot):
    bot.add_cog(Setup(bot))