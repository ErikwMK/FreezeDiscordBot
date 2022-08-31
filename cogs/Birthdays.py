import discord
from discord.ext import commands, tasks
from discord import app_commands

from datetime import datetime
import json
from random import choice

from cogs.StaticMethods import StaticMethods


with open("cogs/birthdays.json") as birthday_file:
    birthday_data = json.load(birthday_file)

class Birthdays(commands.Cog, StaticMethods):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self.birthdays = birthday_data
        self.CheckBirthday.start()


    @app_commands.command(name="set_birthday", description="Set your Birthday to get pinged when your birthday comes")
    @app_commands.describe(month="The month of your birthday in number format, e. g. 1 for January", day="The day of your birthday in number format, e. g. 24", year="Your age will be mentioned in your Birthday Congratulations. Year in number format, e. g. 2007")
    async def set_birthday(self, interaction: discord.Interaction, month: int, day: int, year: int = None):
        # role = discord.utils.find(lambda r: r.id == 833693177671057418, interaction.guild.roles)
        # if role not in interaction.user.roles:
        #     return await interaction.response.send_message("Only FRZ Members can use this function", ephemeral=True)
        month = await self.AddNull(month)
        day = await self.AddNull(day)
        User = interaction.user.name
        User_id = str(interaction.user.id)
        Date = f"{month}/{day}"
        user_data = {
            "Name": User,
            "id": User_id,
            "Date": Date,
            "Year": year
        }

        with open("cogs/birthdays.json") as f:
            data = json.load(f)
            data[User_id] = user_data
        return await interaction.response.send_message("Done!", ephemeral=True)

    @app_commands.command(name="remove_birthday", description="[Staff Only] Removes the Birthday data of a Member")
    @app_commands.describe(user="The user whose birthday you want to remove")
    async def remove_birthday(self, interaction: discord.Interaction, user: discord.User):
        if "manage_messages" not in [perm[0] for perm in interaction.user.guild_permissions if perm[1]]:
            return interaction.response.send_message("You dont have the permission to do this!", ephemeral=True)
        user_id = user.id
        with open("cogs/birthdays.json") as f:
            data = json.load(f)
            del data["birthdays"][user_id]
        await interaction.response.send_message("Done", ephemeral=True)

    @tasks.loop(hours=1)
    async def CheckBirthday(self):
        full_datetime = datetime.now()
        hour = full_datetime.strftime("%H")
        day = full_datetime.strftime("%m/%d")
        year = full_datetime.strftime("%Y")
        if hour != "14":
            return
        for i in self.birthdays["birthdays"]:
            if day == self.birthdays["birthdays"][i]["Date"]:
                user = i
                break
        else:
            return

        mention = f"<@{self.birthdays['birthdays'][user]['id']}>"

        brithday_msg_list = [f"Happy Birthday {mention}! 🥳",
                             f"{mention} Happy Birthday King",
                             f"Best wishes for your Birthday {mention}! 🎉"]
        if year is not None:
            user_year = self.birthdays["birthdays"][user]["Year"]
            age = await self.ToTextNumber(int(year) - int(user_year))
            brithday_msg_list = [f"Happy {age} Birthday {mention}! 🥳",
                                 f"{mention} Happy {age} Birthday King 😎",
                                 f"Best wishes for your {age} Birthday {mention}! 🎉"]
        birthday_msg = choice(brithday_msg_list)

        guild = await self.bot.fetch_guild(746014047866191932)
        channel = await guild.fetch_channel(820129866950901790)

        await channel.send(birthday_msg)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Birthdays(bot),
        guild=discord.Object(id=952331580544806993)
    )
