import asyncio
import datetime
import os
import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.embedbuilder import buildEmbed, buildErrorMessage
import discord.ui as ui
from manager.Ticket import Ticket, getCurrentTicketID, getAllOpenTickets
import utils.database as db
import discord.utils
import utils.settingsgetter as settingsgetter
from dateutil import tz
ticket = None

class TicketView(ui.View):


    @ui.button(label="Schließen", style=discord.ButtonStyle.red, custom_id="closeticketbutton")
    async def closebutton_callback(self, button, interaction):
        global ticket
        await interaction.channel.send(embed=buildEmbed(title="Ticket geschlossen", text="Dein Ticket wurde erfolgreich geschlossen!\nDer Channel wird in 5 Sekunden geschlossen", color=0xFF5151))

        messages = await interaction.message.channel.history(limit=200, oldest_first=True).flatten()
        r = False
        with open(f"id-{ticket.ticketid}.txt", "w", encoding="utf-8") as f:
            for message in messages:
                if not message.author.bot:
                    if str(message.content) != "":
                        r = True
                        f.write(f"[{message.created_at.astimezone(tz.gettz('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')}] {str(message.author.display_name)}: {str(message.content)}\n")
        if r == True:
            await interaction.guild.get_channel(int(settingsgetter.getLogChannelID(ticket.ticketformular))).send(embed=buildEmbed(title="Ticket Log", text=f"""
            ID: {ticket.ticketid}
            Owner: {interaction.guild.get_member(ticket.ownerid).name}#{interaction.guild.get_member(ticket.ownerid).discriminator}
            Channel ID: {ticket.channelid}
            Erstellt: {datetime.datetime.fromtimestamp(ticket.timestamp).astimezone(tz.gettz('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')}
            Geschlossen: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Moderator: {"Keiner" if ticket.modid == 0 else interaction.guild.get_member(ticket.modid).name}
            Betreff: {ticket.concern}
            Formular: {ticket.ticketformular}
            Geschlossen von: {interaction.user.author.name}#{interaction.user.discriminator}
            Genaues Anliegen: 
            ```{ticket.detailedconcern}```
            """), file = discord.File(f'id-{ticket.ticketid}.txt'))
            os.remove(f'id-{ticket.ticketid}.txt')
        else:
            await interaction.guild.get_channel(int(settingsgetter.getLogChannelID(ticket.ticketformular))).send(
                embed=buildEmbed(title="Ticket Log", text=f"""
                        ID: {ticket.ticketid}
                        Owner: {interaction.guild.get_member(ticket.ownerid).name}#{interaction.guild.get_member(ticket.ownerid).discriminator}
                        Channel ID: {ticket.channelid}
                        Erstellt: {datetime.datetime.fromtimestamp(ticket.timestamp).astimezone(tz.gettz('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')}
                        Geschlossen: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        Moderator: {"Keiner" if ticket.modid == 0 else interaction.guild.get_member(ticket.modid).name}
                        Betreff: {ticket.concern}
                        Formular: {ticket.ticketformular}
                        Geschlossen von: {interaction.user.name}#{interaction.user.discriminator}
                        Genaues Anliegen: 
                        ```{ticket.detailedconcern}```
                        """))
        await asyncio.sleep(5)
        await interaction.channel.delete()
        db.updateData("tickets", "state='closed'", f"ticketid={ticket.ticketid}")


class CreateModal(ui.Modal):

    def __init__(self) -> None:

        super().__init__(title="Ticket erstellen")
        self.add_item(ui.InputText(label="Betreff", placeholder="Schreibe hier den Betreff / Oberbegriff des Ticket rein", required=True, style=discord.InputTextStyle.short))
        self.add_item(ui.InputText(label="Genaues Anliegen", placeholder="Schreibe hier dein genaues Anliegen rein", required=True, style=discord.InputTextStyle.long))


    async def callback(self, interaction: discord.Interaction):
        global ticket
        opentickets = getAllOpenTickets()
        ownerids = []
        for item in opentickets:
            if(item[8] == db.convertData(db.getData("ticketsettings", "ticketname", f"createchannel = '{interaction.channel.id}'")[0], "str")):
                ownerids.append(int(item[1]))
        if interaction.user.id in ownerids:
            await interaction.response.send_message(embed=buildErrorMessage(
                                                                     text=f"Du hast bereits ein offenes Ticket. Bitte schließe es zuerst bevor du ein neues erstellst."), ephemeral=True)
            return

        _ticketid = getCurrentTicketID()
        _ticketid += 1
        _channel = await interaction.guild.create_text_channel(f'『✉️』ticket-{interaction.user.name}',
                                                       category=interaction.channel.category, reason="Ticket erstellt | ID: " + str(_ticketid))
        await _channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await _channel.set_permissions(interaction.guild.get_role(int(settingsgetter.getTeamRoleID(db.convertData(db.getData("ticketsettings", "ticketname", f"createchannel = '{interaction.channel.id}'")[0], "str")))), view_channel=True)
        await _channel.set_permissions(interaction.user, view_channel=True)

        await _channel.send(content=f"<@{str(interaction.user.id)}>", embed=buildEmbed("Ticket #" + str(_ticketid), text=f"Willkommen in deinem Ticket <@{str(interaction.user.id)}>!\n_ _\n**Betreff:** {self.children[0].value}\n**Genaues Anliegen:**\n ```{self.children[1].value}```"), view=TicketView())
        ticket = Ticket(ticketid=_ticketid, ownerid=interaction.user.id, channelid=_channel.id, timestamp=datetime.datetime.utcnow().timestamp(), concern=self.children[0].value, detailedconcern=self.children[1].value, ticketformular=db.convertData(db.getData("ticketsettings", "ticketname", f"createchannel = '{interaction.channel.id}'"), "str"))
        await interaction.response.send_message(embed=buildEmbed(title="Ticket erstellt", text=f"Dein Ticket wurde erfolgreich erstellt!\n**ID:** {ticket.ticketid}\n**Channel:** <#{ticket.channelid}>\n**Betreff:** {ticket.concern}\n**Genaues Anliegen:**\n ```{ticket.detailedconcern}```", emojiu="✅"), ephemeral=True)


class CreateButtonClick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.custom_id == "createticketbutton":
            await interaction.response.send_modal(CreateModal())


def setup(bot):
    bot.add_cog(CreateButtonClick(bot))