import datetime
from datetime import datetime, timezone, timedelta
import aiohttp

import discord
from discord import app_commands
from discord.ext import commands

from SirenBot import *
from functions import *


class Events(commands.Cog):
    def __init__(self, bot:SirenBot):
        self.bot = bot
    
    # Complete, need QA
    @commands.Cog.listener(name='on_webhooks_update')
    async def webhook_updates(self, channel):
        """
        If a webhook gets created, modified, or deleted,
        Mega alert gets sent.
        """

        if channel.guild.id != get_guild_id():
            return
                
        time_ago = discord.utils.utcnow() - timedelta(seconds=50)
        webhook_create, webhook_delete, webhook_update = [], [], []

        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.webhook_create, limit=1, after=time_ago):
            webhook_create.append(entry)

        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.webhook_delete, limit=1, after=time_ago):
            webhook_delete.append(entry)

        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.webhook_update, limit=1, after=time_ago):
            webhook_update.append(entry)

        # Need to update.
        if webhook_create != []:
            entry = webhook_create[0]

            for webhook in await channel.guild.webhooks():
                if webhook.id == entry.target.id:
                    webhook_obj = webhook
                    break

            embed = discord.Embed(title='Webhook created', description=f'A webhook has been created in {webhook_obj.channel.mention}.', color=self.bot.color)
            embed.add_field(name='Created by:', value=f'{entry.user.mention}\n{entry.user}\n{entry.user.id}')
            embed.add_field(name='Webhook Name:', value='`{}`'.format(webhook_obj.name))
            embed.set_image(url=webhook_obj.display_avatar)
            
            embed.set_footer(text='Displayed above is the webhook avatar.')
            await send_webhook_embed('mega_alerts', embed)
            
        # Complete, need QA
        if webhook_delete != []:
            entry = webhook_delete[0]

            embed = discord.Embed(title='Webhook deleted', description=f'A webhook has been deleted.', color=self.bot.color)
            embed.add_field(name='Deleted by:', value=f'{entry.user.mention}\n{entry.user}\n{entry.user.id}')
            embed.add_field(name='Webhook Name:', value=entry.before.name)
            embed.set_image(url=entry.before.avatar)

            embed.set_footer(text='Displayed above is the webhook avatar.')
            await send_webhook_embed('mega_alerts', embed)
            
        # Complete, need QA
        if webhook_update != []:
            entry = webhook_update[0]

            for webhook in await channel.guild.webhooks():
                if webhook.id == entry.target.id:
                    webhook_obj = webhook
                    break
    
            embed = discord.Embed(title='Webhook updated', description=f'A webhook has been updated in {webhook_obj.channel.mention}.', color=self.bot.color)
            embed.add_field(name='Updated by:', value=f'{entry.user.mention}\n{entry.user}\n{entry.user.id}')
            
            """Checking if the webhook name was updated"""
            desc_name = None
            try:
                desc_name = f'**Before:** `{entry.before.name}`\n' \
                    + f'**After:** `{entry.after.name}`'
            except AttributeError:
                desc_name = '`{}`'.format(webhook_obj.name)

            embed.add_field(name='Webhook Name:', value=desc_name)

            """Everything else"""
            embed.set_image(url=webhook_obj.display_avatar)

            embed.set_footer(text='Displayed above is the webhook avatar.')
            await send_webhook_embed('mega_alerts', embed)

    # Complete, need QA
    @commands.Cog.listener(name='on_guild_leave')
    async def sirenbot_leaves_guild(self, guild):
        """
        If the bot leaves the guild, 
        Mega alert gets sent.
        """

        if guild.id != get_guild_id():
            return

        embed = discord.Embed(title=f'Bot Left {guild.name}', description=f'{self.bot.user.mention} has just left {guild.name}.', color=self.bot.color, timestamp=discord.utils.utcnow())
        await send_webhook_embed('mega_alerts', embed)

    # Fix bug where embed gets sent even when perm is set to TRUE
    @commands.Cog.listener(name='on_guild_channel_update')
    async def general_locked(self, before, after):
        if before.guild.id != get_guild_id():
            return

        """Getting objects."""
        mega_alert_logs = self.bot.get_channel(get_mega_alert_logs()) if get_mega_alert_logs() != 0 else None

        if mega_alert_logs is None:
            print('Error in general_locked: You haven\'t added a channel ID to MEGA_ALERT_LOGS, have you?\n Add it in config.env ASAP and restart the bot.')
            return

        general_chat = self.bot.get_channel(get_gen_chat())
        verified_role = before.guild.get_role(get_verified_role())
        everyone_role = before.guild.default_role

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
        await mega_alert_logs.send(embed=embed)

    # Complete, need QA
    @commands.Cog.listener(name='on_guild_role_create')
    async def scary_role_created(self, role):
        """
        If any role is created with scary permissions,
        Mega alert gets sent.
        """

        if role.guild.id != get_guild_id():
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

        if len(role_scary_permissions) == 0:
            return

        embed = discord.Embed(title='Scary role created', description=f'`{role.name}` has just been created with `{len(role_scary_permissions)}` scary permission{"s" if len(role_scary_permissions) != 1 else ""}.', color=self.bot.color, timestamp=discord.utils.utcnow())
        embed.add_field(name='Permissions:', value='\n'.join(role_scary_permissions))
        
        async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_create, limit=1):
            embed.add_field(name='Created by:', value=f'{entry.user.mention}\n{entry.user}\n{entry.user.id}')

        await send_webhook_embed('mega_alerts', embed)

    # Complete, need QA
    @commands.Cog.listener(name='on_guild_role_update')
    async def scary_role_updated(self, before, after):
        """
        If any role is given scary permissions,
        Critical alert gets sent.
        """

        if before.guild.id != get_guild_id():
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

        embed = discord.Embed(title='Scary role updated', description=f'`{after.name}` ({after.mention}) has just been given `{len(role_scary_permissions)}` scary permission{"s" if len(role_scary_permissions) != 1 else ""}.', color=self.bot.color, timestamp=discord.utils.utcnow())
        embed.add_field(name='Permissions:', value='\n'.join(role_scary_permissions))

        async for entry in before.guild.audit_logs(action=discord.AuditLogAction.role_update, limit=1):
            embed.add_field(name='Updated by:', value=f'{entry.user.mention}\n{entry.user}\n{entry.user.id}')
        
        await send_webhook_embed('mega_alerts', embed)

    # Complete, need QA
    @commands.Cog.listener(name='on_member_update')
    async def watched_roles_given(self, before, after):
        """
        If any of the watched roles (admin, moderator, team) are given,
        Critical alert gets sent.
        """

        if before.guild.id != get_guild_id():
            return

        watched_roles = {before.guild.get_role(get_admin_role()), before.guild.get_role(get_mod_role()), before.guild.get_role(get_team_role())}
    
        """When someone RECEIVES a watched role, it gets logged."""
        if set(after.roles).difference(set(before.roles)):
            different_role = set(after.roles).difference(set(before.roles))
            different_role = list(different_role)[0]

            if different_role not in watched_roles:
                return

            embed = discord.Embed(title='Watched role given', description=f'{different_role.mention} has been given to {after.mention}.', color=self.bot.color, timestamp=discord.utils.utcnow())
            embed.set_author(name=after, icon_url=after.avatar)
            embed.set_footer(text=f'User ID: {after.id}')
            await send_webhook_embed('critical', embed)
        
        


        

async def setup(bot):
    await bot.add_cog(Events(bot))