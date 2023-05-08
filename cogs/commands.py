import discord
import sqlite3
from sqlite3 import Error
from discord import app_commands
from discord.ext import commands
from typing import *

from SirenBot import *
from functions import *


class Commands(commands.Cog):
    def __init__(self, bot: SirenBot):
        self.bot = bot

    # Complete
    @commands.hybrid_command(description='Creates 3 logging webhooks in the channels from `config.env`. Administrator privileges required.')
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):     
        """
        ## Command is ran in the guild with the logs

        Checks if ctx.author is 'bot_master' from config.env
            If they aren't, return
            If they are, continue

        Checks if there are webhooks titled 'mega', 'critical', 'general' anywhere in the server
            If there is, it deletes them

        Creates 3 webhooks titled 'mega', 'critical', and 'general' in the corresponding channels from config.env
            If it encounters a perms issue, sends a response & return
        Stores the webhook URLs in webhook_tokens.json
        
        Sends a response
        """
        
        """Checks if there are webhooks titled 'mega', 'critical', 'general' anywhere in the server"""
        for webhook in await ctx.guild.webhooks():
            if webhook.name in ['SB Mega Alert Logs', 'SB Critical Logs', 'SB General Logs']:
                await webhook.delete()
                continue

        general_channel = self.bot.get_channel(get_general_logs()) if get_general_logs() != 0 else None
        critical_channel = self.bot.get_channel(get_critical_logs()) if get_critical_logs() != 0 else None
        mega_alert_channel = self.bot.get_channel(get_mega_alert_logs()) if get_mega_alert_logs() != 0 else None

        if None in [general_channel, critical_channel, mega_alert_channel]:
            embed = discord.Embed(title=self.bot.swr, description=self.bot.no_logs, color=self.bot.color)
            await ctx.send(embed=embed)
            return
    
        """Creates 3 webhooks titled 'mega', 'critical', and 'general' in the corresponding channels from config.env"""
        try:
            general_webhook = await general_channel.create_webhook(name='SB General Logs', avatar=await self.bot.user.avatar.read())
            update_webhook_tokens_json('general', general_webhook.url)

            critical_webhook = await critical_channel.create_webhook(name='SB Critical Logs', avatar=await self.bot.user.avatar.read())
            update_webhook_tokens_json('critical', critical_webhook.url)

            mega_alert_webhook = await mega_alert_channel.create_webhook(name='SB Mega Alert Logs', avatar=await self.bot.user.avatar.read())
            update_webhook_tokens_json('mega_alerts', mega_alert_webhook.url)
        except Exception as e:
            print(e)
            embed = discord.Embed(title=self.bot.swr, description='Please ensure you have given me the `Manage Webhooks` permission in the 3 desired channels.', color=self.bot.color)
            await ctx.send(embed=embed)
            return
        
        """Sending a response"""
        embed = discord.Embed(description=f'Successfully created 3 logging webhooks in {general_channel.mention}, {critical_channel.mention}, and {mega_alert_channel.mention}.\n\nDo not rename the webhooks.', color=self.bot.color)
        await ctx.send(embed=embed)

    # Complete
    @commands.hybrid_command(description='Displays the current bot config. Administrator privileges required.')
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        """Getting objects."""
        guild = self.bot.get_guild(get_guild_id()) if get_guild_id != None else None
        general_chat = self.bot.get_channel(get_gen_chat()) if get_gen_chat != None else None
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

        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=f'Bot ID: {self.bot.user.id}')
        await ctx.send(embed=embed)

    # Complete
    @commands.hybrid_command(description='Check the bot\'s permissions to ensure proper function. Administrator privileges required.')
    @commands.has_permissions(administrator=True)
    async def checkperms(self, ctx):
        if ctx.guild.id != get_guild_id():
            return
        
        """Getting all permissions from the bot"""
        bot_member_obj = ctx.guild.get_member(self.bot.user.id)
        required_perms = ['read_messages', 'view_audit_log', 'manage_webhooks', 'send_messages', 'embed_links', 'read_message_history']
        
        desc = ''
        for (permission, value) in bot_member_obj.guild_permissions:
            if permission in required_perms and value is True:
                desc += f'✅ {permission.replace("_", " ").title()} \n'
            if permission in required_perms and value is False:
                desc += f'❌ {permission.replace("_", " ").title()} \n'

        embed = discord.Embed(title=f'{self.bot.user} Permissions', description='```\n' + desc + '```', color=self.bot.color)
        await ctx.send(embed=embed)
        return

    # Complete
    @commands.hybrid_command(description='Register the config. One-time run only. Administrator privileges required. Slash command only.')
    @commands.has_permissions(administrator=True)
    async def register(self, ctx, modrole: discord.Role, adminrole: discord.Role, teamrole: discord.Role, verifiedrole: discord.Role, generalchannel: discord.TextChannel):
        if not ctx.interaction:
            return
        
        """Toven's work"""
        errored = False
        # connect to the database
        conn = sqlite3.connect("./sirenDB.db")
        cursor = conn.cursor()
        # SQL statement to create the config table upon running command ( also used if config is reset & table deleted )
        sql_create_config_table = """CREATE TABLE IF NOT EXISTS "guild_config" ("guild_id" INTEGER, "mod_role" INTEGER, "admin_role" INTEGER, "team_role" INTEGER, "general_channel" INTEGER, "verified_role" INTEGER, PRIMARY KEY("guild_id"));"""
        cursor.execute(sql_create_config_table)
        # Command takes the snowflake ID of various Discord base classes and stores them in the sqlitedb for later retrieval in event classes
        # start by getting the command's context guild id
        guild = ctx.guild.id
        # convert the Role objects to their IDs
        modrole_id, adminrole_id, teamrole_id, verifiedrole_id = modrole.id, adminrole.id, teamrole.id, verifiedrole.id
        # convert the Channel object to ID
        generalchannel_id = generalchannel.id
        # try to insert the provided settings into the database. throws sqlite Error if guild_id exists in DB
        try:
            cursor.execute("INSERT INTO guild_config(guild_id, mod_role, admin_role, team_role, general_channel, verified_role) VALUES ({}, {}, {}, {}, {}, {})".format(guild, modrole_id, adminrole_id, teamrole_id, generalchannel_id, verifiedrole_id))
            conn.commit()
        # catch sqlite specific "Error" if unique guild_id constraint violated
        except Error:
            cursor.execute("SELECT * FROM guild_config WHERE guild_id = {}".format(guild))
            config = cursor.fetchall()
            errored = True
            await ctx.send("ERROR: Bot has already been set up. Config:\n{}".format(config))
        # show the user the config when it does run
        cursor.execute("SELECT * FROM guild_config WHERE guild_id = {}".format(guild))
        config = cursor.fetchall()
        if not errored:
            """Pattles' work (just the return embed)"""
            embed = discord.Embed(description='Database configured. Config:\n```{}```\n'.format(config) + f'Use `{self.bot.prefix}config` to review your config at any time.', color=self.bot.color)
            await ctx.send(embed=embed)
        

    # Complete
    @commands.command(description="Syncs all commands globally. Administrator privileges required. Text command only.")
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if ctx.author.id not in self.bot.developer_ids:
            return

        embed = discord.Embed(description="Syncing...", color=self.bot.color)
        msg = await ctx.send(embed=embed)
        print("Syncing...")
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await msg.edit(embed=discord.Embed(description=f"Synced `{len(synced)}` commands {'globally' if spec is None else 'to the current guild.'}.", color=self.bot.color))
            print("Synced.")
            return
        
        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await msg.edit(embed=discord.Embed(description=f"Synced the tree to {ret}/{len(guilds)}.", color=self.bot.color))
        print("Synced.")


async def setup(bot):
    await bot.add_cog(Commands(bot))
