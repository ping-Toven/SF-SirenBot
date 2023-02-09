import datetime
from datetime import datetime, timezone

import discord
import sqlite3
from discord import app_commands
from discord.ext import commands

from SirenBot import *
from functions import *


class Commands(commands.Cog):
    def __init__(self, bot:SirenBot):
        self.bot = bot

    @commands.command(description='Say hello to the bot.')
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}!')
    

async def setup(bot):
    await bot.add_cog(Commands(bot))