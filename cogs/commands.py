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

    @commands.hybrid_command(description='Displays the current bot config.')
    async def config(self, ctx):
        guild = self.bot.get_guild(get_guild_id())
        general_chat = self.bot.get_channel(get_gen_chat())

        desc = f'**Guild ID:** {guild.id} \n' \
            + f'**Mod Role:** {""} \n' \
            + f'**Admin Role:** {""} \n' \
            + f'**Team Role:** {""} \n' \
            + f'**General Channel:** {""} \n' \
            + f'**Verified Role:** {""} \n' \
            + f'**Log Channel:** {""} \n' \
            + f'**Log Webhook:** {""} \n'

        # Commented out until I decide which embed style looks best.

        embed = discord.Embed(title=f'{guild.name} Config', description=desc, color=discord.Color.random())
        # embed.add_field(name='Guild:', value=guild.id)
        # embed.add_field(name='#general', value=
        #    general_chat.mention + '\n' \
        #    + '#' + general_chat.name + '\n' \
        #    + '`' + str(general_chat.id) + '`'
        #    )
        
        await ctx.send(embed=embed)
        pass
    

async def setup(bot):
    await bot.add_cog(Commands(bot))