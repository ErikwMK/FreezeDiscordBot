import discord
from discord.ext import commands

import json


with open("config.json") as f:
    config = json.load(f)


class PingHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == "<@926801089989333012>":
            embed = discord.Embed(title="{config['BOT_NAME']}", colour=discord.Colour((config["MAIN_COLOR"])))
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/699904940231098459/879355861376573500/reFRZtransparent.png")
            embed.add_field(name="**Description**", value=f"The FRZ Bot is a Discord Bot made by {config['CREATOR_NAME']} to analyse the stats of any map played in 6v6", inline=False)
            embed.add_field(name=f"**Requirements**", value=f"> You have to use Toadbot\n> You must have one channel for Toadbot stuff\n*else the bot is basically useless for your server*\nAlso, if you are chatting a lot in the selected toadbot channel, it falsifies the result!", inline=False)
            embed.add_field(name=f"**Setup**", value=f"Use `/setchannel` and `/Set_permissions_for_stats64_command`. Everything explained below!", inline=False)

            embed2 = discord.Embed(title="Setup Commands", colour=discord.Colour((config["MAIN_COLOR"])))
            embed2.add_field(name=f"`/setchannel`", value=f"Sets the default Toadbot channel of your server. It's changeable when using commands.\nCommand `/setchannel <DiscordChannel>`", inline=False)
            embed2.add_field(name=f"`/Set_permissions_for_stats64_command`", value=f"Sets the Permissions, if everyone or only Leaders can use the spammy /stats64 command.\nCommand `/Set_permissions_for_stats64_command <Everyone/Only_Leaders>`", inline=False)

            embed3 = discord.Embed(title="Stats Commands", colour=discord.Colour((config["MAIN_COLOR"])))
            embed3.add_field(name=f"`/mapstats`", value=f"Shows the stats of a specific map of a certain amount of wars\nCommand `/mapstats <map> <amount_of_wars> <toadchannel>`\n> `<map>` short form of any MK8DX map. e. g. MKS, rmmm, bNH\n> `<amount_of_wars>` The amount of wars where stats should be analysed. For performance its highly recommended to use this feature!\n> `<toadchannel>` Overwrites the default toadchannel, so you can use another one.", inline=False)
            embed3.add_field(name=f"`/map`", value=f"Shows the races of a specific map of a certain amount of wars\nCommand `/map <map> <amount_of_wars> <toadchannel>`\n> `<map>` short form of any MK8DX map. e. g. MKS, rmmm, bNH\n> `<amount_of_wars>` The amount of wars where stats should be analysed. For performance its highly recommended to use this feature!\n> `<toadchannel>` Overwrites the default toadchannel, so you can use another one.`", inline=False)
            embed3.add_field(name=f"`/overallstats`", value=f"Shows the stats of a every map of a certain amount of wars\nCommand `/overallstats <amout_of_wars> <toadchannel>`\n> `<amount_of_wars>` The amount of wars where stats should be analysed. For performance its highly recommended to use this feature!\n> `<toadchannel>` Overwrites the default toadchannel, so you can use another one.", inline=False)
            embed3.add_field(name=f"`/stats56`", value=f"Shows the stats of every map of a certain amount entered\nCommand`/stats56 <amount_of_wars> <toadchannel> `\n> `<ampunt_of_wars>` The amount of wars where stats should be analysed. For performance its highly recommended to use this feature!\n> `<toadchannel>` Overwrites the default toadchannel, so you can use another one.\nThe channel will be spammed quickly, make sure to have it disabled that not leaders (people with manage_messages permission) can use this command if you want to!", inline=False)
            embed3.set_footer(text="Bot made by {config['CREATOR_NAME']}", icon_url="https://images-ext-1.discordapp.net/external/DYve2PXS45DrDa9wFHlSCPGAMS0VBIAhouo5GX9dMoU/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/807602307369271306/ad65fc359ed1f554aa2f7e23cc42330c.png?width=676&height=676")

            await ctx.channel.send(embeds=[embed, embed2, embed3])
            return


async def setup(bot):
    await bot.add_cog(
        PingHelp(bot)
    )
