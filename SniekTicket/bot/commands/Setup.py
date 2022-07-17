import datetime

import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.embedbuilder import buildEmbed
import discord.ui as ui
from manager.Ticket import Ticket
import utils.database as db

class CreateModal(ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="Ticket erstellen")
        self.add_item(ui.InputText(label="Betreff", placeholder="Schreibe hier den Betreff / Oberbegriff des Ticket rein", required=True, style=discord.InputTextStyle.short))
        self.add_item(ui.InputText(label="Genaues Anliegen", placeholder="Schreibe hier dein genaues Anliegen rein", required=True, style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        ticket = Ticket(ticketid=10, ownerid=interaction.user.id, channelid=990748555381735444, timestamp=datetime.datetime.utcnow().timestamp(), concern=self.children[0].value, detailedconcern=self.children[1].value)
        await interaction.response.send_message(embed=buildEmbed(title="Ticket erstellt", text=f"Dein Ticket wurde erfolgreich erstellt!\n**ID:** {ticket.ticketid}\n**Channel:** <#{ticket.channelid}>\n**Betreff:** {ticket.concern}\n**Genaues Anliegen:**\n ```{ticket.detailedconcern}```", emojiu="✅"), ephemeral=True)




class CreateView(ui.View):


    @ui.button(label="Ticket erstellen", style=discord.ButtonStyle.green, emoji="📨", custom_id="createticketbutton")
    async def sendbutton_callback(self, button, interaction):
        return



class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="setup", description="setup command")
    async def _setup(self, ctx: discord.ApplicationContext, name: discord.Option(str, required=True), channel: discord.Option(discord.TextChannel,  required=True), logchannel: discord.Option(discord.TextChannel,  required=True), teamrole: discord.Option(discord.Role,  required=True)):

        if(db.checkData( "ticketsettings", "createchannel", "ticketname = '{}'".format(name))):
            await ctx.send("Diese Ticket Config ist schon vergeben!")
            return
        db.insertData("ticketsettings", "ticketname, createchannel, logchannel, teamroleid", f"'{name}', {channel.id}, {logchannel.id}, {teamrole.id}")
        embed = buildEmbed(title="Ticket System", text="\n_ _\nÖffne ein Ticket indem du auf den Knopf unten drückst!\n_⚠️ Ticket-Absuse wird mit einem Warn bestraft ⚠️_")
        embed.set_image(url="https://i.imgur.com/hOFmd6M.png")
        await channel.send(embed=embed, view=CreateView())




def setup(bot):
    bot.add_cog(Setup(bot))