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