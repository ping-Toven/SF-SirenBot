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
    
    # Complete
    @commands.Cog.listener(name='on_webhooks_update')
    async def webhook_updates(self, channel):
        """
        If a webhook gets created, modified, or deleted,
        Mega alert gets sent.
        """
        if channel.guild.id != get_guild_id():
            return


        time_ago = discord.utils.utcnow() - timedelta(seconds=60)
        webhook_create, webhook_delete, webhook_update = [], [], []

        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.webhook_create, limit=1, after=time_ago):
            webhook_create.append(entry)

        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.webhook_delete, limit=1, after=time_ago):
            webhook_delete.append(entry)

        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.webhook_update, limit=1, after=time_ago):
            webhook_update.append(entry)
        

        # Complete
        if webhook_create != []:
            entry = webhook_create[0]

            for webhook in await channel.guild.webhooks():
                if webhook.id == entry.target.id:
                    webhook_obj = webhook
                    break

            embed = discord.Embed(title='Webhook created', description=f'A webhook has been created in {webhook_obj.channel.mention}.', color=self.bot.color, timestamp=discord.utils.utcnow())
            embed.add_field(name='Created by:', value=f'{entry.user.mention}\n{entry.user}\n{entry.user.id}')
            embed.add_field(name='Webhook Name:', value='`{}`'.format(webhook_obj.name))
            embed.set_image(url=webhook_obj.display_avatar)
            
            embed.set_footer(text='Displayed above is the webhook avatar.')
            await send_webhook_embed('mega_alerts', embed)
            
        # Complete
        if webhook_delete != []:
            entry = webhook_delete[0]

            embed = discord.Embed(title='Webhook deleted', description=f'A webhook has been deleted.', color=self.bot.color, timestamp=discord.utils.utcnow())
            embed.add_field(name='Deleted by:', value=f'{entry.user.mention}\n{entry.user}\n{entry.user.id}')
            embed.add_field(name='Webhook Name:', value=entry.before.name)
            embed.set_image(url=entry.before.avatar)

            embed.set_footer(text='Displayed above is the webhook avatar.')
            await send_webhook_embed('mega_alerts', embed)
            
        # Complete
        if webhook_update != []:
            entry = webhook_update[0]

            for webhook in await channel.guild.webhooks():
                if webhook.id == entry.target.id:
                    webhook_obj = webhook
                    break
            

            embed = discord.Embed(title='Webhook updated', description=f'A webhook has been updated in {webhook_obj.channel.mention}.', color=self.bot.color, timestamp=discord.utils.utcnow())
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

    # Complete
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

    # Complete
    @commands.Cog.listener(name='on_guild_channel_update')
    async def general_locked(self, before, after):
        """
        If @everyone or @verified loses send_messages or view_channel permissions in #general,
        Mega alert gets sent.
        """
        
        if before.guild.id != get_guild_id():
            return
        
        general_chat = self.bot.get_channel(get_gen_chat())
        verified_role = before.guild.get_role(get_verified_role())

        """Checking if the channel updated is general_chat."""
        if before.id != general_chat.id:
            return
                
        """Checks if general_chat is locked."""        
        everyone_perms_dict = dict(general_chat.overwrites.get(before.guild.default_role))
        verified_perms_dict = dict(general_chat.overwrites.get(verified_role))

        check_perms = [everyone_perms_dict.get('read_messages'), everyone_perms_dict.get('send_messages'), verified_perms_dict.get('read_messages'), verified_perms_dict.get('send_messages')]

        if False not in check_perms:
            return

    
        """Sending embed to logging channel."""
        embed = discord.Embed(title=f'#{general_chat} has just been locked.', description=f'[Jump!]({general_chat.jump_url})', color=self.bot.color, timestamp=discord.utils.utcnow())

        async for entry in before.guild.audit_logs(action=discord.AuditLogAction.channel_update, limit=1):
            embed.add_field(name='Locked by:', value=f'{entry.user.mention}\n{entry.user}\n{entry.user.id}')

        await send_webhook_embed('mega_alerts', embed)

    # Complete
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

    # Complete
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

    # Complete
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
        
    # Complete
    @commands.Cog.listener(name='on_member_remove')
    async def watched_members_removed(self, member):
        """
        If a member with any of the watched roles leaves the server (kick, ban, or of their own accord),
        Mega alert gets sent.
        """
        if member.guild.id != get_guild_id():
            return

        
        watched_roles = {member.guild.get_role(get_admin_role()), member.guild.get_role(get_mod_role()), member.guild.get_role(get_team_role())}
        member_roles = {role for role in member.roles}

        if not member_roles.intersection(watched_roles):
            return
        
        watched_roles_lost = list(member_roles.intersection(watched_roles))

        """Send embed"""
        embed = discord.Embed(title=f'Watched member left {member.guild.name}', color=self.bot.color, timestamp=discord.utils.utcnow())
        embed.add_field(name='Watched roles left with:', value=' '.join(role.mention for role in watched_roles_lost))
        embed.set_author(name=member, icon_url=member.avatar)
        embed.set_footer(text=f'User ID: {member.id}')
        
        async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick, limit=1):
            if entry.target == member:
                embed.add_field(name='Reason for leaving:', value=f'{member.name} left was **kicked** by {entry.user} (`{entry.user.id}`) {f"with reason `{entry.reason}`" if entry.reason else "without a reason"}.')
                await send_webhook_embed('mega_alerts', embed)
                return
            
        async for entry in member.guild.audit_logs(action=discord.AuditLogAction.ban, limit=1):
            if entry.target == member:
                embed.add_field(name='Reason for leaving:', value=f'{member.name} left was **banned** by {entry.user} (`{entry.user.id}`) {f"with reason `{entry.reason}`" if entry.reason else "without a reason"}.')
                await send_webhook_embed('mega_alerts', embed)
                return

        embed.add_field(name='Reason for leaving:', value='Their own accord.')
        await send_webhook_embed('mega_alerts', embed)

    # Complete
    @commands.Cog.listener(name='on_member_update')
    async def watched_members_roles_removed(self, before, after):
        """
        If users with any of the watched roles (admin, moderator, team) lose any roles,
        Mega alert gets sent.
        """
        if before.guild.id != get_guild_id():
            return
        
        if before.roles == after.roles:
            return
        
        watched_roles = {before.guild.get_role(get_admin_role()), before.guild.get_role(get_mod_role()), before.guild.get_role(get_team_role())}

        if not set(before.roles).intersection(watched_roles):
            return

        if not set(before.roles).difference(set(after.roles)):
            return

        different_role = set(before.roles).difference(set(after.roles))
        different_role = list(different_role)[0]

        embed = discord.Embed(title='Watched member lost a role', color=self.bot.color, timestamp=discord.utils.utcnow())
        embed.add_field(name='Role lost:', value=different_role.mention)
        embed.set_author(name=before, icon_url=before.avatar)
        embed.set_footer(text=f'User ID: {before.id}')

        await send_webhook_embed('mega_alerts', embed)
        
    # Complete
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(description='Visit the [documentation](https://sirenbot.gitbook.io/sirenbot-documentation/) for instructions on how to setup the bot.', color=self.bot.color)
        
        for channel in guild.channels:
            if type(channel) == discord.TextChannel:
                try:
                    await channel.send(embed=embed)
                    return
                except:
                    continue
            
        


        

async def setup(bot):
    await bot.add_cog(Events(bot))