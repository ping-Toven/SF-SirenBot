import datetime
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from SirenBot import *
from functions import *


class Events(commands.Cog):
    def __init__(self, bot:SirenBot):
        self.bot = bot
    
    """Need to figure out how to differentiate between webhook being created, updated, or deleted."""
    @commands.Cog.listener(name='on_webhooks_update')
    async def webhook_updates(self, channel):
        """Getting objects."""
        logging_channel = self.bot.get_channel(get_log_channel()) if get_log_channel() != None else 0
        
        if logging_channel == 0:
            return

        # Useful links:
        # https://discordpy.readthedocs.io/en/stable/api.html#discord.on_webhooks_update
        # https://discordpy.readthedocs.io/en/stable/api.html#discord.Webhook
        
        """Getting the most recent webhook."""
        webhooks = await channel.webhooks()
        recent_webhook = sorted(webhooks, key=lambda x: x.created_at, reverse=True)[0]

        """Sending embed to the logging channel."""
        embed = discord.Embed(title='Webhook updated', description=f'A webhook has been updated in {channel.mention}.', color=self.bot.color, timestamp=discord.utils.utcnow())
        embed.add_field(name='Webhook Author:', value=
            recent_webhook.user.mention + '\n' + recent_webhook.user.name + '\n' + str(recent_webhook.user.id)
            )
        embed.add_field(name='Webhook Name:', value=recent_webhook.name)
        embed.set_image(url=recent_webhook.display_avatar)
        embed.set_footer(text='Displayed above is the webhook avatar.')

        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name='on_guild_leave')
    async def sirenbot_leaves_guild(self, guild):
        """Getting objects."""
        logging_channel = self.bot.get_channel(get_log_channel()) if get_log_channel() != None else 0
        guild_from_db = self.bot.get_guild(get_guild_id()) if get_guild_id() != None else 0
        
        if logging_channel == 0:
            return

        if guild_from_db == 0:
            embed = discord.Embed(title=self.bot.swr, description=f'There is no guild defined in config.', color=self.bot.color)

            # Replace with a defined error channel. Waiting for toven to add to db.
            await logging_channel.send(embed=embed)
            return

        """Sending embed to logging channel."""
        embed = discord.Embed(title=f'Bot Left {guild.name}', description=f'{self.bot.user.mention} has just left {guild.name}.', color=self.bot.color, timestamp=discord.utils.utcnow())

        await logging_channel.send(embed=embed)
        pass        

    """Need to add verified role, fix small issue then complete"""
    @commands.Cog.listener(name='on_guild_channel_update')
    async def general_locked(self, before, after):
        """Getting objects."""
        logging_channel = self.bot.get_channel(get_log_channel()) if get_log_channel() != None else 0
        
        if logging_channel == 0:
            return

        general_chat = self.bot.get_channel(get_gen_chat()) if get_gen_chat() != None else 0
        verified_role = before.guild.get_role(get_verified_role() if get_verified_role() != None else 0)
        everyone_role = before.guild.default_role

        if general_chat == 0:
            embed = discord.Embed(self.bot.swr, description='There is no general chat defined in config.', color=self.bot.color)
            
            # Replace with a defined error channel. Waiting for toven to add to db.
            await logging_channel.send(embed=embed)
            return
        
        if verified_role == 0:
            embed = discord.Embed(title=self.bot.swr, description='There is no verified role defined in config.', color=self.bot.color)

            # Replace with a defined error channel. Waiting for toven to add to db.
            await logging_channel.send(embed=embed)
            return

        """Checking if the channel updated is general_chat."""
        if before.id != general_chat.id:
            return

        """Checks general_chat is locked."""
        # Need to add a check for if permission is set to neutral.
        permissions_check = [after.permissions_for(verified_role).view_channel, after.permissions_for(verified_role).send_messages, after.permissions_for(everyone_role).view_channel, after.permissions_for(everyone_role).send_messages]
        if all(permissions_check):
            return
        
        """Sending embed to logging channel."""
        embed = discord.Embed(title=f'#{general_chat} has just been locked.', description=f'[Jump!]({general_chat.jump_url})', color=self.bot.color, timestamp=discord.utils.utcnow())
        embed.set_footer(text=f'Guild ID: {before.guild.id}')
        await logging_channel.send(embed=embed)

    """Need to get role creator, but I don't want to go into Audit Log"""
    @commands.Cog.listener(name='on_guild_role_create')
    async def scary_role_created(self, role):
        if role.guild.id != get_guild_id():
            return

        """Getting objects."""
        logging_channel = self.bot.get_channel(get_log_channel()) if get_log_channel() != None else 0
        
        if logging_channel == 0:
            return

        """Getting all enabled permissions from role."""
        role_true_permissions = []
        for (permission, value) in role.permissions:
            if value is True:
                role_true_permissions.append(permission)

        """Getting all scary permissions from role."""
        role_scary_permissions = []
        for permission in role_true_permissions:
            if permission in ['administrator', 'manage_roles', 'mention_everyone', 'manage_webhooks', 'manage_channels', 'manage_guild']:
                temp = permission.replace('_', ' ')
                role_scary_permissions.append(temp.title())

        embed = discord.Embed(title='Scary role created', description=f'`{role.name}` has just been created with `{len(role_scary_permissions)}` scary permission{"s" if len(role_scary_permissions) != 1 else ""}.', color=self.bot.color, timestamp=discord.utils.utcnow())
        embed.add_field(name='Permissions:', value='\n'.join(role_scary_permissions))
        
        # Need to go into the Audit Log to check who created a role.
        # It's a huge pain, so I'll won't be doing it (for now, at least).
        # embed.add_field(name='Created by:', value='')

        await logging_channel.send(embed=embed)

    """  """
    @commands.Cog.listener(name='on_guild_role_update')
    async def scary_role_updated(self, before, after):
        if before.guild.id != get_guild_id():
            return

        """Getting objects."""
        logging_channel = self.bot.get_channel(get_log_channel()) if get_log_channel() != None else 0
        
        if logging_channel == 0:
            return

        if before.permissions == after.permissions:
            return

        """Getting all enabled permissions from updated role."""
        role_true_permissions = []
        for (permission, value) in after.permissions:
            if value is True:
                role_true_permissions.append(permission)

        """Getting all scary permissions from updated role."""
        role_scary_permissions = []
        for permission in role_true_permissions:
            if permission in ['administrator', 'manage_roles', 'mention_everyone', 'manage_webhooks', 'manage_channels', 'manage_guild']:
                temp = permission.replace('_', ' ')
                role_scary_permissions.append(temp.title())

        if len(role_scary_permissions) == 0:
            return

        embed = discord.Embed(title='Scary role created', description=f'`{after.name}` has just been given `{len(role_scary_permissions)}` scary permission{"s" if len(role_scary_permissions) != 1 else ""}.', color=self.bot.color, timestamp=discord.utils.utcnow())
        embed.add_field(name='Permissions:', value='\n'.join(role_scary_permissions))
        
        # Need to go into the Audit Log to check who created a role.
        # It's a huge pain, so I'll won't be doing it (for now, at least).
        # embed.add_field(name='Created by:', value='')

        await logging_channel.send(embed=embed)

        

async def setup(bot):
    await bot.add_cog(Events(bot))