import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from discord.utils import find

import json


def LoadAllGuildObjects():
    all_guild_objects = []

    with open("cogs/data.json") as guilds:
        data = json.load(guilds)
        for i in data["data"]:
            guild_id = str(i)
            guild_object = discord.Object(id=guild_id)
            all_guild_objects.append(guild_object)
    return all_guild_objects

def GetToadbot(guild):
    with open("cogs/data.json") as f:
        data = json.load(f)
        channel = data["data"][guild]["default_toadbot_channel_id"]
    return channel

def GetPermsStats56(guild):
    with open("cogs/data.json") as f:
        data = json.load(f)
        perms = data["data"][guild]["perms_stats56"]
    return perms

class SetupBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def AddServer(server):
        with open("cogs/data.json", "r") as f:
            data = json.load(f)
        new_data = {
            "server_id": server.id,
            "server_name": server.name,
            "default_toadbot_channel_id": None,
            "perms_stats56": True
        }
        data["data"][str(server.id)] = new_data
        with open("cogs/data.json", "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    async def SearchForChat(guild):
        general = find(
            lambda x: x.name.lower() == 'general' or x.name.lower() == "chat" or x.name.lower() == "allgemein",
            guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send('Thanks for the invite!\n@me for help')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.AddServer(guild)
        await self.SearchForChat(guild)

    @staticmethod
    async def SetToadbot(server_id, toadbot):
        with open("cogs/data.json", "r") as f:
            data = json.load(f)
            data["data"][server_id]["default_toadbot_channel_id"] = toadbot
        with open("cogs/data.json", "w") as f:
            json.dump(data, f, indent=4)
        return

    @app_commands.command(name="setup-default-toadbot-channel", description="[Leader only] Sets your default Toadbot channel for the commands")
    @app_commands.guild_only()
    async def SetToadbotCommand(self, interaction: discord.Interaction, toad_channel: discord.TextChannel):
        if "manage_messages" not in [perm[0] for perm in interaction.user.guild_permissions if perm[1]]:
            await interaction.response.send_message("You don't have the permission to use this!", ephemeral=True)
            return
        await self.SetToadbot(str(interaction.guild.id), toad_channel.id)
        await interaction.response.send_message("Done!", ephemeral=True)

    @staticmethod
    async def SetPermsStats56(server_id, setting):
        with open("cogs/data.json", "r") as f:
            data = json.load(f)
            data["data"][server_id]["perms_stats56"] = setting
        with open("cogs/data.json", "w") as f:
            json.dump(data, f, indent=4)
        return

    @app_commands.choices(
        setting=[
            Choice(name="Only Leaders", value="only_leaders"),
            Choice(name="Everyone", value="everyone"),
        ]
    )
    @app_commands.command(name="setup-permission-stats64-command", description="[Leader only] Allow either only Leaders to use the spammy stats64 command or everyone")
    @app_commands.guild_only()
    async def Set_permissions_for_stats64_command(self, interaction: discord.Interaction, setting: Choice[str]):
        if "manage_messages" not in [perm[0] for perm in interaction.user.guild_permissions if perm[1]]:
            await interaction.response.send_message("You don't have the permission to use this!", ephemeral=True)
            return
        if setting.value == "only_leaders":
            setting = True
        elif setting.value == "everyone":
            setting = False
        await self.SetPermsStats56(str(interaction.guild.id), setting)
        await interaction.response.send_message("Done!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(
        SetupBot(bot),
    )