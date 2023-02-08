import datetime
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands

from SirenBot import *


class Events(commands.Cog):
    def __init__(self, bot:SirenBot):
        self.bot = bot
    
    """Needs logging channel code, then complete"""
    @commands.Cog.listener(name='on_webhooks_update')
    async def webhook_updates(self, channel):
        # send_channel exists purely for testing purposes. Replace with a channel from db.
        send_channel = self.bot.get_channel(964572977234595910)

        # Useful links:
        # https://discordpy.readthedocs.io/en/stable/api.html#discord.on_webhooks_update
        # https://discordpy.readthedocs.io/en/stable/api.html#discord.Webhook
        
        """Getting the most recent webhook."""
        webhooks = await channel.webhooks()
        recent_webhook = sorted(webhooks, key=lambda x: x.created_at, reverse=True)[0]

        """Sending embed to the logging channel."""
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
        pass

    """Needs logging channel code, then complete"""
    @commands.Cog.listener(name='on_guild_leave')
    async def sirenbot_leaves_guild(self, guild):
        # send_channel exists purely for testing purposes. Replace with a channel from db.
        send_channel = self.bot.get_channel(964572977234595910)

        """Sending embed to logging channel."""
        embed = discord.Embed(title=f'Bot Left {guild.name}', description=f'{self.bot.user.mention} has just left {guild.name}.', color=discord.Color.random(), timestamp=discord.utils.utcnow())

        await send_channel.send(embed=embed)

        # await channel.send(embed=embed)
        # Will need to get logging channel info from db, waiting for Toven to create db
        pass        

    """Needs logging channel code & fix small issue, then complete"""
    @commands.Cog.listener(name='on_guild_channel_update')
    async def general_locked(self, before, after):
        # send_channel exists purely for testing purposes. Replace with a channel from db.
        send_channel = self.bot.get_channel(964572977234595910)

        # Replace with a channel from db.
        general_chat = self.bot.get_channel(964572977234595910)

        """Checking if the channel updated is general_chat."""
        if before.id != general_chat.id:
            return

        """Getting role objects."""
        everyone_role = before.guild.default_role
        
        # Replace with verified role from db.
        verified_role = before.guild.get_role(1065417951391531110)

        """Checks general_chat is locked."""
        # Need to add a check for if permission is set to neutral.
        permissions_check = [after.permissions_for(verified_role).view_channel, after.permissions_for(verified_role).send_messages, after.permissions_for(everyone_role).view_channel, after.permissions_for(everyone_role).send_messages]
        if all(permissions_check):
            return
        
        """Sending embed to logging channel."""
        embed = discord.Embed(title=f'#{general_chat} has just been locked.', description=f'[Jump!]({general_chat.jump_url})', color=discord.Color.random(), timestamp=discord.utils.utcnow())
        embed.set_footer(text=f'Guild ID: {before.guild.id}')
        await send_channel.send(embed=embed)

        # await channel.send(embed=embed)
        # Will need to get logging channel info from db, waiting for Toven to create db.
        pass 

async def setup(bot):
    await bot.add_cog(Events(bot))