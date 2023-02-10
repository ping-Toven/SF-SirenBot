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

    """Incomplete"""
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

    """Incomplete"""
    @commands.command(description='Check if the bot is missing any permissions for it to work properly.')
    async def permscheck(self, ctx):
        if ctx.guild.id != get_guild_id():
            return

        bot_member_obj = ctx.guild.get_member(self.bot.user.id)

        """Getting all permissions from bot.."""
        bot_permissions = ''
        for (permission, value) in bot_member_obj.guild_permissions:
            if value is True:
                bot_permissions += f'✅ {permission} \n'
            else:
                bot_permissions += f'❌ {permission} \n'

        embed = discord.Embed(title=f'{self.bot.user} Permissions', description=bot_permissions, color=self.bot.color)
        await ctx.send(embed=embed)








    

async def setup(bot):
    await bot.add_cog(Commands(bot))