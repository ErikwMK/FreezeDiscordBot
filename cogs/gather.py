import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

from cogs.StaticMethods import StaticMethods


class gather(commands.Cog, StaticMethods):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.choices(
        format=[
            Choice(name="relative", value="R"),
            Choice(name="short time", value="t"),
            Choice(name="song time", value="T"),
            Choice(name="short date", value="d"),
            Choice(name="long date", value="D"),
            Choice(name="long date with short time", value="f"),
            Choice(name="long date with day of week and short time", value="F")
        ]
    )
    @app_commands.command(name="timestamp", description="create an timestamp")
    @app_commands.describe(hour="Hour in timezone CEST")
    async def timestamp(self, interaction: discord.Interaction, hour: int, format: Choice[str]):
        timestamp = await self.create_timestamp(hour, format.value)
        await interaction.response.send_message(f"`{timestamp}`", ephemeral=True)

    @app_commands.command(name="gather", description="Default gather-messages for the times 19, 20, 21, 22 CEST. Option Times: 20 21 23, Range: 18-23")
    @commands.guild_only()
    async def gather(self, interaction: discord.Interaction, times: str = None, time_range: str = None):
        if "manage_messages" not in [perm[0] for perm in interaction.user.guild_permissions if perm[1]]:
            return await interaction.response.send_message("You dont have the permission for that", ephemeral=True)

        if times is None and time_range is None:
            times = [19, 20, 21, 22]
        elif times and time_range:
            return await interaction.response.send_message("You cant use both parameters!", ephemeral=True)
        elif times and time_range is None:
            times = times.split(" ")
        elif times is None and time_range:
            try:
                time_range = time_range.split("-", 1)
                time1 = int(time_range[0])
                time2 = int(time_range[1])
                int(time1)
                int(time2)
            except ValueError:
                return await interaction.response.send_message("The range is invalid! Use for example `20-23`", ephemeral=True)
            if not 0 <= time1 <= 23 and 0 <= time2 <= 23:
                return await interaction.response.send_message("The range is invalid! Use for example `20-23`", ephemeral=True)
            times = []
            if time1 < time2:
                for i in range(time1, time2 + 1):
                    times.append(i)
            elif time1 > time2:
                for i in range(time1, 24):
                    times.append(i)
                for i in range(0, time2 + 1):
                    times.append(i)
            else:
                times.append(time1)

        for i in times:
            try:
                int(i)
            except ValueError:
                return await interaction.response.send_message("One of the times is invalid! Use for example `20 21 22`", ephemeral=True)
            if not 0 <= int(i) <= 23:
                return await interaction.response.send_message("One of the times is invalid! Use for example `20 21 22`", ephemeral=True)

        await interaction.response.defer(ephemeral=False)
        to_delete_msg = await interaction.followup.send("Gathering")
        for i in times:
            await interaction.channel.send(await self.create_timestamp(int(i), "t"))

        ping = None
        if interaction.channel.id == 983056553164804166:  # frz1
            ping = "<@&982594404470648864> <@&833693270089007184>"
        elif interaction.channel.id == 983057182901809212: # frz2
            ping = "<@&982594480320442448> <@&833693270089007184>"
        elif interaction.channel.id == 963044201552031765: # all
            ping = "<@&833693177671057418> <@&833693270089007184>"

        if ping is not None:
            await interaction.channel.send(ping)
        await to_delete_msg.delete()
        return

    @commands.command(name="opponent", description="Removes opponent if opponent field is empty, otherwise it adds a (new) opponent")
    @commands.guild_only()
    async def opponent(self, ctx, *args):
        opponent = f" ".join(args)
        if "manage_messages" not in [perm[0] for perm in ctx.author.guild_permissions if perm[1]]:
            return await ctx.message.delete()
        if ctx.message.reference is None:
            return await ctx.message.delete()
        reference_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if reference_msg.author != self.bot.user:
            return await ctx.message.delete()
        if len(args) != 0:
            await ctx.message.delete()
            if "vs" in reference_msg.content:
                return await reference_msg.edit(content=reference_msg.content.split(" vs ")[0] + f" vs {opponent}")
            return await reference_msg.edit(content=reference_msg.content + f" vs {opponent}")
        await ctx.message.delete()
        return await reference_msg.edit(content=reference_msg.content.split(" ")[0])


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        gather(bot),
        guild=discord.Object(id=746014047866191932)
    )
