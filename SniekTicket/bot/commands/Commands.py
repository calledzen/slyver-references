import asyncio
import datetime
import os
import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.embedbuilder import buildEmbed
import discord.ui as ui
from manager.Ticket import getAllOpenTickets
import utils.database as db
import discord.utils
import utils.settingsgetter as settingsgetter
from dateutil import tz

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="close", description="Schließt ein Ticket")
    async def _close(self, ctx: discord.ApplicationContext, ticketid: discord.Option(int, required=False), channel: discord.Option(discord.TextChannel, required=False)):

        if discord.utils.get(ctx.guild.roles, id=int(os.getenv('TEAM_ID'))) in ctx.author.roles:
            opentickets = getAllOpenTickets()
            channelsids = []
            ticketids = []
            for item in opentickets:
                channelsids.append(int(item[2]))
                ticketids.append(int(item[0]))
            if ticketid is None:

                if int(channel.id) in channelsids:
                    ticketdata = None
                    for item in opentickets:
                        if (item[2] == str(channel.id)):
                            ticketdata = item
                            break

                    await channel.send(embed=buildEmbed(title="Ticket geschlossen",
                                                                    text="Dein Ticket wurde erfolgreich geschlossen!\nDer Channel wird in 5 Sekunden geschlossen",
                                                                    color=0xFF5151))

                    messages = await channel.history(limit=200, oldest_first=True).flatten()
                    r = False
                    with open(f"id-{ticketdata[0]}.txt", "w", encoding="utf-8") as f:
                        for message in messages:
                            if not message.author.bot:
                                if str(message.content) != "":
                                    r = True
                                    f.write(
                                        f"[{message.created_at.astimezone(tz.gettz('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')}] {str(message.author.display_name)}: {str(message.content)}\n")
                    if r == True:
                        await channel.guild.get_channel(
                            int(settingsgetter.getLogChannelID(ticketdata[8]))).send(
                            embed=buildEmbed(title="Ticket Log", text=f"""
                                ID: {ticketdata[0]}
                                Owner: {channel.guild.get_member(int(ticketdata[1])).name}#{channel.guild.get_member(int(ticketdata[1])).discriminator}
                                Channel ID: {ticketdata[2]}
                                Erstellt: {datetime.datetime.fromtimestamp(float(ticketdata[3])).astimezone(tz.gettz('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')}
                                Geschlossen: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                                Moderator: {"Keiner" if int(ticketdata[4]) == 0 else channel.guild.get_member(int(ticketdata[4])).name}
                                Betreff: {ticketdata[6]}
                                Formular: {ticketdata[8]}
                                Geschlossen von: {ctx.author.name}#{ctx.author.discriminator}
                                Genaues Anliegen: 
                                ```{ticketdata[7]}```
                                """), file=discord.File(f'id-{ticketdata[0]}.txt'))
                        os.remove(f'id-{ticketdata[0]}.txt')
                    else:
                        await channel.guild.get_channel(
                            int(settingsgetter.getLogChannelID(ticketdata[8]))).send(
                            embed=buildEmbed(title="Ticket Log", text=f"""
                                                        ID: {ticketdata[0]}
                                                        Owner: {channel.guild.get_member(int(ticketdata[1])).name}#{channel.guild.get_member(int(ticketdata[1])).discriminator}
                                                        Channel ID: {ticketdata[2]}
                                                        Erstellt: {datetime.datetime.fromtimestamp(float(ticketdata[3])).astimezone(tz.gettz('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')}
                                                        Geschlossen: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                                                        Moderator: {"Keiner" if int(ticketdata[4]) == 0 else channel.guild.get_member(int(ticketdata[4])).name}
                                                        Betreff: {ticketdata[6]}
                                                        Formular: {ticketdata[8]}
                                                        Geschlossen von: {ctx.author.name}#{ctx.author.discriminator}
                                                        Genaues Anliegen: 
                                                        ```{ticketdata[7]}```
                                                        """))
                    await asyncio.sleep(5)
                    await channel.delete()
                    db.updateData("tickets", "state='closed'", f"ticketid={ticketdata[0]}")


            elif int(ticketid) in ticketids:
                ticketdata = None
                for item in opentickets:
                    if (item[0] == ticketid):
                        ticketdata = item
                        break
                channel = self.bot.get_channel(int(ticketdata[2]))
                await channel.send(embed=buildEmbed(title="Ticket geschlossen",
                                                    text="Dein Ticket wurde erfolgreich geschlossen!\nDer Channel wird in 5 Sekunden geschlossen",
                                                    color=0xFF5151))

                messages = await channel.history(limit=200, oldest_first=True).flatten()
                r = False
                with open(f"id-{ticketdata[0]}.txt", "w", encoding="utf-8") as f:
                    for message in messages:
                        if not message.author.bot:
                            if str(message.content) != "":
                                r = True
                                f.write(
                                    f"[{message.created_at.astimezone(tz.gettz('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')}] {str(message.author.display_name)}: {str(message.content)}\n")
                if r == True:
                    await channel.guild.get_channel(
                        int(settingsgetter.getLogChannelID(ticketdata[8]))).send(
                        embed=buildEmbed(title="Ticket Log", text=f"""
                                                ID: {ticketdata[0]}
                                                Owner: {channel.guild.get_member(int(ticketdata[1])).name}#{channel.guild.get_member(int(ticketdata[1])).discriminator}
                                                Channel ID: {ticketdata[2]}
                                                Erstellt: {datetime.datetime.fromtimestamp(float(ticketdata[3])).astimezone(tz.gettz('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')}
                                                Geschlossen: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                                                Moderator: {"Keiner" if int(ticketdata[4]) == 0 else channel.guild.get_member(int(ticketdata[4])).name}
                                                Betreff: {ticketdata[6]}
                                                Formular: {ticketdata[8]}
                                                Geschlossen von: {ctx.author.name}#{ctx.author.discriminator}
                                                Genaues Anliegen: 
                                                ```{ticketdata[7]}```
                                                """), file=discord.File(f'id-{ticketdata[0]}.txt'))
                    os.remove(f'id-{ticketdata[0]}.txt')
                else:
                    await channel.guild.get_channel(
                        int(settingsgetter.getLogChannelID(ticketdata[8]))).send(
                        embed=buildEmbed(title="Ticket Log", text=f"""
                                                                        ID: {ticketdata[0]}
                                                                        Owner: {channel.guild.get_member(int(ticketdata[1])).name}#{channel.guild.get_member(int(ticketdata[1])).discriminator}
                                                                        Channel ID: {ticketdata[2]}
                                                                        Erstellt: {datetime.datetime.fromtimestamp(float(ticketdata[3])).astimezone(tz.gettz('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')}
                                                                        Geschlossen: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                                                                        Moderator: {"Keiner" if int(ticketdata[4]) == 0 else channel.guild.get_member(int(ticketdata[4])).name}
                                                                        Betreff: {ticketdata[6]}
                                                                        Formular: {ticketdata[8]}
                                                                        Geschlossen von: {ctx.author.name}#{ctx.author.discriminator}
                                                                        Genaues Anliegen: 
                                                                        ```{ticketdata[7]}```
                                                                        """))
                await asyncio.sleep(5)
                await channel.delete()
                db.updateData("tickets", "state='closed'", f"ticketid={ticketdata[0]}")

            else:
                await sendErrorMessage(ctx, "Ticket nicht gefunden")
                return

        else:
            await sendErrorMessage(ctx, "Du hast keine Berechtigung für diesen Befehl")
            return




def setup(bot):
    bot.add_cog(Commands(bot))