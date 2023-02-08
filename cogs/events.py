import datetime
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from SirenBot import *


class Events(commands.Cog):
    def __init__(self, bot:SirenBot):
        self.bot = bot
    
    """Incomplete"""
    @commands.Cog.listener(name='on_guild_role_create')
    async def scary_role_created(self, role):
        # Testing, delete when final.
        channel = role.guild.get_channel(964572977234595910)

        if role.guild.id != 916133196184301668:
            return

        # Final product.
        scary_permissions = [role.permissions.administrator, role.permissions.manage_roles, role.permissions.mention_everyone, role.permissions.manage_webhooks, role.permissions.manage_channels, role.permissions.manage_guild]

        if not any(scary_permissions):
            return

        for permission in role.permissions:
            await channel.send(permission)

        
        embed = discord.Embed(title=f'{role} was created with {"x"} dangerous permissions.', color=discord.Color.random())
        # embed.add_field(name='Permissions:', value='.join(permissions_list)', inline=False)

        # Maybe add a 'who created this role' embed field? - Pattles
        # You will need to use Audit Log though. - Pattles


        # Toven, send this to Jon's channel. - Pattles
        pass

    """Incomplete"""
    @commands.Cog.listener(name='on_guild_role_update')
    async def scary_role_updated(self, before, after):
        # Testing, delete when final.
        channel = before.guild.get_channel(964572977234595910)

        if before.guild.id != 916133196184301668:
            return

        role = before

        # Final product.
        scary_permissions = [role.permissions.administrator, role.permissions.manage_roles, role.permissions.mention_everyone, role.permissions.manage_webhooks, role.permissions.manage_channels, role.permissions.manage_guild]

    @commands.Cog.listener(name='on_webhooks_update')
    async def webhook_updates(self, channel):
        
        # send_channel exists purely for testing purposes. Replace with a channel from db.
        send_channel = self.bot.get_channel(964572977234595910)

        # Useful links:
        # https://discordpy.readthedocs.io/en/stable/api.html#discord.on_webhooks_update
        # https://discordpy.readthedocs.io/en/stable/api.html#discord.Webhook
        
        # Getting the most recent webhook.
        webhooks = await channel.webhooks()
        recent_webhook = sorted(webhooks, key=lambda x: x.created_at, reverse=True)[0]

        # Sending embed to the logging channel.
        embed = discord.Embed(title='Webhook updated', description=f'A webhook has been updated/created/deleted in {channel.mention}.', color=discord.Color.random(), timestamp=discord.utils.utcnow())
        embed.add_field(name='Webhook Author:', value=
            recent_webhook.user.mention + '\n' + recent_webhook.user.name + '\n' + str(recent_webhook.user.id)
            )
        embed.add_field(name='Webhook Name:', value=recent_webhook.name)
        embed.set_image(url=recent_webhook.display_avatar)
        embed.set_footer(text='Displayed above is the webhook avatar.')

        await send_channel.send(embed=embed)

        # await channel.send(embed=embed)
        # Will need to get logging channel info from db, waiting for Toven to create db



    """
    This is if a role with scary permissions is given to a member, which Jon didn't ask for

    @commands.Cog.listener(name='on_member_update')
    async def scary_roles_given(self, before, after):        
        \"\"\"Outdated code below.\"\"\"

        # Testing, delete when final.
        channel = before.guild.get_channel(964572977234595910)

        if before.guild.id != 916133196184301668:
            return

        if not set(after.roles).difference(set(before.roles)):
            return

        # Final product.
        if set(after.roles).difference(set(before.roles)):
            member_roles = set(after.roles).difference(set(before.roles))
            different_role = list(member_roles)[0]
        
        scary_permissions = [different_role.permissions.administrator, different_role.permissions.manage_roles, different_role.permissions.mention_everyone, different_role.permissions.manage_webhooks, different_role.permissions.manage_channels, different_role.permissions.manage_guild]

        if any(scary_permissions):
            await channel.send(True)
    
        return
    """




async def setup(bot):
    await bot.add_cog(Events(bot))