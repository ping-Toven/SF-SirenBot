"""
SF SirenBot by Jon_HQ, Toven, KaoSxEclipse, aaPattles, Alexander, & Bopped
"""


# Add the client ID (the bot's ID) here, or just replace self.client_id directly.
CLIENT_ID = 0

import datetime
import json
import os
import sqlite3
import sys
import traceback
from datetime import datetime, timezone

import discord
from discord.ext import commands
from discord.ext.commands.errors import *
from dotenv import load_dotenv

load_dotenv('token.env')

INITIAL_EXTENSIONS = [
    # "cogs.exampleCog",
    'cogs.events',
    'cogs.testing' # remove this when final
    ]
  
class SirenBot(commands.Bot):
    def __init__(self):
        super().__init__(help_command=MyHelp(command_attrs={'aliases':['h'], 'description':'Displays a list of all available commands. Text command only.'}), command_prefix=commands.when_mentioned_or('sb!'), intents=discord.Intents.all(), case_insensitive=True, activity=discord.Activity(type=discord.ActivityType.watching, name=f'ServerForge'))
        self.client_id = CLIENT_ID
        self.token = os.getenv('TOKEN')

        """Important information"""
        self.prefix = '!'
        self.developer_ids = [165587622243074048, 301494278901989378, 90588733727858688, 675782936728961024, 632252672338165801, 480126550868754465]
        
        self.version = '1.0'

        """Saved Texts, used for simplifying return messages."""
        self.syntax = 'Syntax:'
        self.hyrtcc = 'Uh oh! Have you ran the commmand correctly?'
        self.swr = 'Uh oh! Something went wrong.'
        self.usage = 'Usage:'
        self.aliases = 'Aliases:'
        self.required = '`<> - required`\n'
        self.optional = '`[] - optional`\n'
        self.foobar = '`foo/bar – choose either \'foo\' or \'bar\'`\n'
        self.ratelimited = 'Please wait a few minutes and try again.'


    async def setup_hook(self):
        for extension in INITIAL_EXTENSIONS:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            pass

        if isinstance(error, (MissingRequiredArgument, BadArgument)):
            embed = discord.Embed(title=self.hyrtcc, description=f'Invalid command usage. \n\nFor more information about this command, type `{self.prefix}help {ctx.command.name}`.', color=discord.Color.random())
            
            """Checking if the command has arguments, and therefore required syntax for the embed."""
            required = ''
            optional = ''
            foobar = ''
            if '<' in ctx.command.signature:
                required = '`<> - required`\n'
            if '[' in ctx.command.signature:
                optional = '`[] - optional`\n'
            if '|' in ctx.command.signature:
                foobar = '`item1/item2 - choose either item1 or item2`\n'

            if required != '' or optional != '':
                embed.add_field(name="Syntax:", value=required + optional + foobar, inline=False)
            
            """Adding command usage for the embed."""
            embed.add_field(name=self.usage, value=f'```{self.prefix if "Slash command only." not in ctx.command.description else "/"}{ctx.command} {ctx.command.signature.replace("_", " ")}```', inline=False)
            
            """Checking if the command has an alias for the embed."""
            if ctx.command.aliases:
                embed.add_field(name=self.aliases, value=f'`' + '`, `'.join(ctx.command.aliases) + '`', inline=False)
            await ctx.send(embed=embed)
            
        else:
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    async def on_message(self, message):
        if str(self.user.mention) == message.content:
            if message.author.bot:
                return

            desc = f"I'm {self.user.mention}. My current prefixes are `{self.prefix}` & `/`.\n\n" \
                + f"To view all my commands, type `{self.prefix}help`."
            embed = discord.Embed(description=desc, color=discord.Color.random(), timestamp=discord.utils.utcnow())
            embed.set_footer(text=f"{self.user} • Asked by {message.author}", icon_url=message.author.avatar)
            await message.reply(embed=embed)

        await self.process_commands(message)

    def run(self):
        super().run(self.token, reconnect=True)

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title=f'Help | {self.context.author}', color=discord.Color.random())

        for cog, commands in mapping.items():
            if cog:
                cog_name = cog.qualified_name.replace('_', ' ')

                """Adding embed fields for each command category."""
                """Not displaying hidden categories."""
                if cog_name not in ['Developer', 'Events']:
                    command_list = []
                    for command in commands:
                        command_list.append(command.name)
                    if cog_name in ['General']:
                        command_list.append('help')
                    command_list.sort()
                    command_list = '`, `'.join(command_list)
                    embed.add_field(name=cog_name, value=f'`{command_list}`', inline=False)

                """Displaying hidden categories is author is a developer."""
                if cog_name in ['Developer'] and self.context.author.id in SirenBot.developer_ids:
                    command_list = []
                    for command in commands:
                        command_list.append(command.name)
                    command_list.sort()
                    command_list = '`, `'.join(command_list)
                    embed.add_field(name=cog_name, value=f'`{command_list}`', inline=False)

        embed.set_footer(text=f'Use {SirenBot.prefix}help [command] for more info on a specific command.', icon_url=SirenBot.user.avatar)
        await self.context.reply(embed=embed)
       
    """!help <command>"""
    async def send_command_help(self, command):
        cog_name = command.cog_name
    
        """Cancels the command if the author is attempting to view a command from a hidden category."""
        if cog_name in ['Developer', 'Events'] and self.context.author.id not in SirenBot.developer_ids:
            return

        if command.cog:
            cog_name = cog_name.replace('_', ' ')
    
    
        """Temporary fix for 'help' not displaying under the 'General' category for '!help help'."""
        if command.name in ['help'] and not command.cog:
            cog_name = 'General'

        embed = discord.Embed(title=f'{cog_name} › {command.name}', description=command.description, color=discord.Color.random())
        
        if True:
            required = ''
            optional = ''
            foobar = ''
            if '<' in command.signature:
                required = '`<> - required`\n'
            if '[' in command.signature:
                optional = '`[] - optional`\n'
            if '|' in command.signature:
                foobar = '`item1/item2 - choose either item1 or item2`\n'

        if required != '' or optional != '':
            embed.add_field(name='Syntax:', value=required + optional + foobar, inline=False)

        signature = command.signature.replace("=", "").replace("None", "").replace("...", "").replace("|", "/").replace('"', "").replace("_", " ")
        embed.add_field(name='Usage:', value=f"```{SirenBot.prefix if 'Slash command only.' not in command.description else '/'}{command.name} {signature}```", inline=False)
        
        if command.aliases:
            embed.add_field(name='Aliases:', value='`' + '`, `'.join(command.aliases)+ f'`, `{command.name}`', inline=False)

        embed.set_footer(text=f'Use {SirenBot.prefix}help [command] for more info on a specific command.', icon_url=SirenBot.user.avatar)
        await self.context.reply(embed=embed)
        
      
    """!help <group>"""
    async def send_group_help(self, group):
        return
        await self.context.reply("This is help group")
    
    """!help <cog>"""
    async def send_cog_help(self, cog):
        return
        await self.context.reply("This is help cog")

class Help(commands.Cog):
    def __init__(self, bot: SirenBot) -> None:
        self.bot = bot
        self.bot._original_help_command = bot.help_command
        self.bot.help_command = MyHelp()

    async def cog_unload(self) -> None:
        assert self.bot._original_help_command is not None
        self.bot.help_command = self.bot._original_help_command



if __name__ == '__main__':
    SirenBot = SirenBot()
    SirenBot.run()
