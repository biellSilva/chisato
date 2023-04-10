import discord

from discord import app_commands
from discord.ext import commands
from typing import Optional

from extensions import config


class Help(commands.Cog):

    '''Custom Help Command'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='help')
    async def help_command(self, ctx: commands.Context, input: Optional[str]):
        '''Help Command'''

        if not input:
            emb = discord.Embed(title='Help', color=config.cinza,
                                description=f'Use `{self.bot.command_prefix}help <module>` to gain more information about that module')

            cogs_desc = ''
            for cog in self.bot.cogs:
                if 'error' in cog.lower() or 'on_' in cog.lower():
                    continue

                cogs_desc += f'**{cog}:** *{self.bot.cogs[cog].__doc__}*\n'

            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            commands_desc = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            if commands_desc:
                emb.add_field(name='Not belonging to a module',
                              value=commands_desc, inline=False)

            emb.add_field(name="About", value=f"Developed and maintained by {self.bot.application.owner}, based on discord.py.\n"
                                               "Please visit https://github.com/biellSilva/chisato to submit ideas or bugs.")

        if input:
            for cog in self.bot.cogs:
                if cog.lower() == input.lower():
                    emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
                                        color=config.cinza)

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(
                                name=f"{self.bot.command_prefix}{command.name}", value=command.help, inline=False)
                            
                    for command in self.bot.get_cog(cog).get_app_commands():
                        emb.add_field(
                                name=f"/{command.name}", value=command.description, inline=False)
                    break

        await ctx.send(embed=emb)

async def setup(bot):
    await bot.add_cog(Help(bot))
