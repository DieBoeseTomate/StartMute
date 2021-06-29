import discord
import asyncio


client = discord.Client()


BOT_TOKEN = "Dein Discord Bot Token"


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("TomatiiiBot - .startmute [user] [reason]"))
    print("Bot gestartet : " + client.user.name)


@client.event
async def on_message(message):
    args = message.content.split(" ")
    if message.content == ".src":
        await message.channel.send("https://github.com/DieBoeseTomate/StartMute")
    if message.content == ".ping":
        await message.channel.send(
            embed=discord.Embed(title="Ping", description=client.latency, color=discord.Color.blue()))
    if message.content == ".help":
        await message.channel.send(embed=discord.Embed(title=f"TomatiiiBot",
                                                                 description=f".startmute [@User] [Grund] - Startet eine Abstimmung, ob ein User gemuted werden soll\n"
                                                                             f".ping - zeigt den Ping vom Bot\n", color=discord.Color.blurple()))
    if args[0] == ".startmute":
        if len(args) > 2:
            mentions = message.mentions
            try:
                member = mentions[0]
            except:
                await message.channel.send("Bitte nutze: .startmute [@User] [Grund]")
            if member:
                message = await message.channel.send(embed=discord.Embed(title=f"StartMute gegen {member.name}", description=f"Eine Abstimmung, ob der Nutzer {member.mention} gemuted werden soll, wurde von {message.author.mention} gestartet.\n"
                                                                                                                               f"Grund: `{' '.join(args[2:])}`\n"
                                                                                                                               f"Stimme per Reaktion ab.\n"
                                                                                                                               f"👍 : Ja\n"
                                                                                                                               f"👎 : Nein", color=discord.Color.blue()))
                await message.add_reaction("👍")
                await message.add_reaction("👎")
                await asyncio.sleep(60)
                message = discord.utils.get(client.cached_messages, id=message.id)
                for reaction in message.reactions:
                    if reaction.emoji == "👍":
                        yes_count = reaction.count
                    if reaction.emoji == "👎":
                        no_count = reaction.count
                if yes_count and no_count:
                    if yes_count > no_count:
                        await message.channel.send(embed=discord.Embed(title=f"StartMute gegen {member.name}", description=f"Der Startmute gegen {member.mention} war erfolgreich, da die Mehrheit für einen Mute abgestimmt hat.", color=discord.Color.red()))
                        try:
                            muted = discord.utils.get(message.guild.roles, name="Muted")
                            await member.add_roles(muted)
                            await asyncio.sleep(900)
                            await member.remove_roles(muted)
                        except:
                            await message.channel.send("Keine Rolle mit dem Namen `Muted` gefunden")
                    else:
                        await message.channel.send(embed=discord.Embed(title=f"StartMute gegen {member.name}", description=f"Der Startmute gegen {member.mention} war unerfolgreich, da nicht die Mehrheit für einen Mute abgestimmt hat.", color=discord.Color.green()))
            if not member:
                await message.channel.send(embed=discord.Embed(title="Fehler", description="Der angegebene Nutzer wurde nicht gefunden.", color=discord.Color.red()))
        else:
            await message.channel.send("Bitte nutze: .startmute [@User] [Grund]")


client.run(BOT_TOKEN)
