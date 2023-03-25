import datetime
from datetime import datetime, timezone

import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from typing import *

from SirenBot import *
from functions import *


class Commands(commands.Cog):
    def __init__(self, bot: SirenBot):
        self.bot = bot

    @commands.command(description='Say hello to the bot.')
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}!')

    """Need to figure out who's allowed to use this cmd."""

    @commands.hybrid_command(description='Displays the current bot config.')
    async def config(self, ctx):
        """Getting objects."""
        guild = self.bot.get_guild(get_guild_id()) if get_guild_id != None else None
        general_chat = self.bot.get_channel(get_gen_chat()) if get_gen_chat != None else None
        logging_channel = self.bot.get_channel(get_log_channel()) if get_log_channel != None else None
        mod_role = ctx.guild.get_role(get_mod_role()) if get_mod_role != None else None
        admin_role = ctx.guild.get_role(get_admin_role()) if get_admin_role != None else None
        team_role = ctx.guild.get_role(get_team_role()) if get_team_role != None else None
        verified_role = ctx.guild.get_role(get_verified_role()) if get_verified_role != None else None

        """Sending embed."""
        embed = discord.Embed(title=f'{guild.name} Config', color=self.bot.color)
        embed.add_field(name='Guild:', value=f'{guild.name}\n`{guild.id}`' if guild != None else '`None`')
        embed.add_field(name='Admin Role:',
                        value=f'{admin_role}\n`{admin_role.id}`\n{admin_role.mention}' if admin_role != None else '`None`')
        embed.add_field(name='Mod Role:',
                        value=f'{mod_role}\n`{mod_role.id}`\n{mod_role.mention}' if mod_role != None else '`None`')
        embed.add_field(name='Team Role:',
                        value=f'{team_role}\n`{team_role.id}`\n{team_role.mention}' if team_role != None else '`None`')
        embed.add_field(name='Verified Role:',
                        value=f'{verified_role}\n`{verified_role.id}`\n{verified_role.mention}' if verified_role != None else '`None`')
        embed.add_field(name='General Channel:',
                        value=f'{general_chat}\n`{general_chat.id}`\n{general_chat.mention}' if general_chat != None else '`None`')
        embed.add_field(name='Logging Channel:',
                        value=f'{logging_channel}\n`{logging_channel.id}`\n{logging_channel.mention}' if logging_channel != None else '`None`')

        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=f'Bot ID: {self.bot.user.id}')
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

    @commands.group(invoke_without_command=True, description='Register a role or channel to the config.')
    async def register(self, ctx):
        pass

    @register.command(description="Configure your server's database.")
    async def setupdb(self, ctx: commands.Context, modrole: discord.Role, adminrole: discord.Role, teamrole: discord.Role, verifiedrole: discord.Role, generalchannel: discord.TextChannel):
        # Command takes the snowflake ID of various Discord base classes and stores them in the sqlitedb for later retrieval in event classes
        # start by getting the command's context guild id
        guild = ctx.guild.id
        # convert the Role objects to their IDs
        modrole_id, adminrole_id, teamrole_id, verifiedrole_id = modrole.id, adminrole.id, teamrole.id, verifiedrole.id
        # convert the Channel object to ID
        generalchannel_id = generalchannel.id
        # connect to the database
        conn = sqlite3.connect("sirenDB.db")
        cursor = conn.cursor()
        # try to insert the provided settings into the database. Will not work if guild ID is already in the guild_config table
        try:
            cursor.execute("INSERT INTO guild_config(guild_id, mod_role, admin_role, team_role, general_channel, verified_role) VALUES ({}, {}, {}, {}, {}, {})".format(guild, modrole_id, adminrole_id, teamrole_id, generalchannel_id, verifiedrole_id))
            conn.commit()
        # catch the unique constraint error if trying to run command after setup
        except CommandInvokeError:
            cursor.execute("SELECT * FROM guild_config WHERE guild_id = {}".format(guild))
            config = cursor.fetchall()
            await ctx.send("ERROR: Bot has already been set up. Config:\n{}".format(config))
        # show the user the config when it does run
        cursor.execute("SELECT * FROM guild_config WHERE guild_id = {}".format(guild))
        config = cursor.fetchall()
        await ctx.send("Database configured. Config:\n{}".format(config))

    @register.command(description='Register a moderator role to the config.')
    async def modrole(self, ctx, role: discord.Role):
        # Need code from Toven to add mod_role ID to db.
        await ctx.send(role.mention)

    @register.command(description='Register an administrator role to the config.')
    async def adminrole(self, ctx, role: discord.Role):
        # Need code from Toven to add admin_role ID to db.
        await ctx.send(role.mention)

    @register.command(description='Register a team role to the config.')
    async def teamrole(self, ctx, role: discord.Role):
        # Need code from Toven to add team_role ID to db.
        await ctx.send(role.mention)

    @register.command(description='Register an administrator role to the config.')
    async def verifiedrole(self, ctx, role: discord.Role):
        # Need code from Toven to add verified_role ID to db.
        await ctx.send(role.mention)

    @register.command(description='Register an administrator role to the config.')
    async def generalchannel(self, ctx, channel: discord.TextChannel):
        # Need code from Toven to add general_channel ID to db.
        await ctx.send(channel.mention)


async def setup(bot):
    await bot.add_cog(Commands(bot))
