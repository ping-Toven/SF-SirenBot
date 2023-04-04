import datetime
from datetime import datetime, timezone
import aiohttp

import discord
from discord import app_commands
from discord.ext import commands

from SirenBot import *
from functions import *


class Events(commands.Cog):
    def __init__(self, bot:SirenBot):
        self.bot = bot
    
    # Need to figure out how to differentiate between webhook being created, updated, or deleted."""
    # Need to fix bug where it says there's no channel ID in config.env, even though there is
    @commands.Cog.listener(name='on_webhooks_update')
    async def webhook_updates(self, channel):
        if channel.guild.id != get_guild_id():
            return

        """Getting objects."""
        mega_alert_logs = self.bot.get_channel(get_mega_alert_logs()) if get_mega_alert_logs() != 0 else None

        if mega_alert_logs is None:
            print('Error in webhook_updates: You haven\'t added a channel ID to MEGA_ALERT_LOGS, have you?\n Add it in config.env ASAP and restart the bot.')
            return
        
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

        await mega_alert_logs.send(embed=embed)

    @commands.Cog.listener(name='on_guild_leave')
    async def sirenbot_leaves_guild(self, guild):
        if guild.id != get_guild_id():
            return

        embed = discord.Embed(title=f'Bot Left {guild.name}', description=f'{self.bot.user.mention} has just left {guild.name}.', color=self.bot.color, timestamp=discord.utils.utcnow())
        await send_webhook_embed('mega_alerts', embed)

    """Fix bug where embed gets sent even when perm is set to TRUE"""
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

    """Need to get role creator, but I don't want to go into Audit Log"""
    @commands.Cog.listener(name='on_guild_role_create')
    async def watched_role_created(self, role):
        if role.guild.id != get_guild_id():
            return

        """Getting objects."""
        mega_alert_logs = self.bot.get_channel(get_mega_alert_logs()) if get_mega_alert_logs() != 0 else None

        if mega_alert_logs is None:
            print('Error in watched_role_created: You haven\'t added a channel ID to MEGA_ALERT_LOGS, have you?\n Add it in config.env ASAP and restart the bot.')
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

        await mega_alert_logs.send(embed=embed)

    """Need to get role creator, but I don't want to go into Audit Log"""
    @commands.Cog.listener(name='on_guild_role_update')
    async def watched_role_updated(self, before, after):
        if before.guild.id != get_guild_id():
            return

        """Getting objects."""
        mega_alert_logs = self.bot.get_channel(get_mega_alert_logs()) if get_mega_alert_logs() != 0 else None

        if mega_alert_logs is None:
            print('Error in watched_role_updated: You haven\'t added a channel ID to MEGA_ALERT_LOGS, have you?\n Add it in config.env ASAP and restart the bot.')
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

        await mega_alert_logs.send(embed=embed)

    @commands.Cog.listener(name='on_member_update')
    async def watched_roles_given(self, before, after):
        if before.guild.id != get_guild_id():
            return

        """Getting objects."""
        critical_logs = self.bot.get_channel(get_critical_logs()) if get_critical_logs() != 0 else None

        if critical_logs is None:
            print('Error in watched_roles_given: You haven\'t added a channel ID to CRITICAL_LOGS, have you?\n Add it in config.env ASAP and restart the bot.')
            return

        watched_roles = {before.guild.get_role(get_admin_role()), before.guild.get_role(get_mod_role()), before.guild.get_role(get_team_role())}
    
        """When someone RECEIVES a watched role, it gets logged."""
        if set(after.roles).difference(set(before.roles)):
            different_role = set(after.roles).difference(set(before.roles))
            different_role = list(different_role)[0]

            if different_role not in watched_roles:
                return

            if not critical_logs:
                print('Error in watched_roles_given: You haven\'t added a channel ID to CRITICAL_LOGS, have you?\n Add it in config.env ASAP.')
                return

            embed = discord.Embed(title='Watched role given', description=f'{different_role.mention} has been given to {after.mention}.', color=self.bot.color, timestamp=discord.utils.utcnow())
            embed.set_author(name=after, icon_url=after.avatar)
            embed.set_footer(text=f'User ID: {after.id}')
            await critical_logs.send(embed=embed)
        
        


        

async def setup(bot):
    await bot.add_cog(Events(bot))