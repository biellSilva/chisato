import discord

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
            em = discord.Embed(title='Help', color=config.cinza,
                                description=f'Use `{self.bot.command_prefix}help <module>` to gain more information about that module')

            cogs_desc = ''
            for cog in self.bot.cogs:
                if len(self.bot.cogs[cog].get_commands()) == 0 and len(self.bot.cogs[cog].get_app_commands()) == 0:
                    continue

                cogs_desc += f'**{cog}:** *{self.bot.cogs[cog].__doc__}*\n'

            em.add_field(name='Modules', value=cogs_desc, inline=False)

            em.add_field(name="About", value=f"Developed and maintained by {self.bot.application.owner}\n"
                                              "https://github.com/biellSilva/chisato")

        if input:
            for cog in self.bot.cogs:
                if cog.lower() == input.lower():
                    em = discord.Embed(title=f'{cog} Commands', description=self.bot.cogs[cog].__doc__,
                                        color=config.cinza)

                    for command in self.bot.get_cog(cog).walk_commands():
                        if not command.hidden and command.enabled:
                            em.add_field(
                                name=f"{self.bot.command_prefix}{command.name}", value=command.help, inline=False)
                            
                    for command in self.bot.get_cog(cog).walk_app_commands():
                        em.add_field(name=f"/{command.qualified_name}", value=command.description, inline=False)

                    break

        await ctx.send(embed=em)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
