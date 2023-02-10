import datetime
from datetime import datetime, timezone

import discord
from discord import app_commands
from discord.ext import commands
from typing import *

from SirenBot import *
from functions import *


class Developer(commands.Cog):
    def __init__(self, bot:SirenBot):
        self.bot = bot

    @commands.command(description="Syncs all commands globally. Only accessible to developers.")
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
    await bot.add_cog(Developer(bot))