import discord
from discord.ext import commands

import asyncio


class BotStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await self.bot.change_presence(activity=discord.Game("@me for help!"))
            await asyncio.sleep(10)
            await self.bot.change_presence(activity=discord.Game("Bro, its cold in here 🥶"))
            await asyncio.sleep(4)

async def setup(bot):
    await bot.add_cog(
        BotStatus(bot)
    )
