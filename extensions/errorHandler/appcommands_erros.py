import discord
import traceback

from discord.ext import commands
from discord import app_commands
from discord.app_commands import AppCommandError
from traceback import print_exception
from sys import stderr
from time import time

from extensions import config
from extensions.utils import DatetimeFomartError, InvalidHexFormat, NotMentionableRole


class AppErrorHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def cog_load(self):
        tree = self.bot.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.on_app_command_error

    def cog_unload(self):
        tree = self.bot.tree
        tree.on_error = self._old_tree_error

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, err: AppCommandError):

        em = discord.Embed(color=config.cinza,
                           description='')

        if isinstance(err, app_commands.CommandInvokeError):
            err = err.original

        if isinstance(err, app_commands.CommandNotFound):
            return

        if isinstance(err, app_commands.MissingPermissions):
            em.description='\n'.join(err.args)

        if isinstance(err, app_commands.MissingRole):
            em.description=f'Missing role {interaction.guild.get_role(int(err.missing_role)).mention}'
        
        if isinstance(err, app_commands.BotMissingPermissions):
            em.description='\n'.join(err.args)

        if isinstance(err, app_commands.CommandOnCooldown):
            em.description = f'Command on cooldown\n<t:{int(time() + err.retry_after)}:R>' 

        if isinstance(err, NotImplementedError):
            em.description = f'Not implemented yet'

        if isinstance(err, discord.Forbidden):
            if err.code == 50007:
                em.description = 'I can\'t send DM\'s to you, try allowing to receive DM\'s from here'
        
        if isinstance(err, discord.HTTPException):
            if err.code in (50035, 50138):
                em.description = err.text

        if isinstance(err, DatetimeFomartError):
            em.description = (f'**{err.date_str}** does not correspond to a datetime format\n\n'
                              f'Expected:\n'
                              f'`dd/mm/yyyy HH:MM` -> **day/month/year hour:minute**\n'
                              f'`dd/mm/yyyy` -> **day/month/year 21:00**\n'
                              f'`HH:MM` -> **today HH:MM**')
            
        if isinstance(err, InvalidHexFormat):
            em.description = (f'Invalid HEX format: **{err.hex}**\n'
                              'Expected: **#20B2AA**')

        if isinstance(err, NotMentionableRole):
            em.description = f'{err.role} is not mentionable'




        if em.description != '' and interaction.response.is_done():
            await interaction.edit_original_response(embed=em)

        elif em.description != '' and not interaction.response.is_done():
            await interaction.response.send_message(embed=em, ephemeral=True)

        else:
            txt_err = ''.join(traceback.format_exception(type(err), err, err.__traceback__))
            txt_err = f'```{txt_err}```'

            if len(txt_err) < 2000:
                await self.bot.application.owner.send(txt_err)
            else:
                await self.bot.application.owner.send(f'```Error\n{err}```')

            print(file=stderr)
            print_exception(type(err), err, err.__traceback__, file=stderr)


async def setup(bot: commands.Bot):
    await bot.add_cog(AppErrorHandler(bot))
