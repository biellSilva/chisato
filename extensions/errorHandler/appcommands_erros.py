import discord

from discord.ext import commands
from discord import app_commands
from discord.app_commands import AppCommandError
from traceback import print_exception
from sys import stderr

from extensions import config
from extensions.bgcolors import bcolors


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
        em.set_footer(text=f'{interaction.user.display_name} - {interaction.user.id}',
                      icon_url=interaction.user.display_avatar.url)

        if isinstance(err, app_commands.MissingPermissions):
            em.description=f'Missing permission'
            return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)

        if isinstance(err, app_commands.MissingRole):
            em.description=f'Missing role {interaction.guild.get_role(int(err.missing_role)).mention}'
            return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)

        print(f'\n{bcolors.WARNING}{"! ! "*30}\n'
              f'{bcolors.FAIL}{interaction.command} exception: ', file=stderr)
        print_exception(type(err), err, err.__traceback__, file=stderr)
        print(bcolors.ENDC)


async def setup(bot):
    await bot.add_cog(AppErrorHandler(bot))