import datetime
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from SirenBot import *


class Commands(commands.Cog):
    def __init__(self, bot:SirenBot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.mention}')
    

async def setup(bot):
    await bot.add_cog(Commands(bot))