import discord

from discord.ext import commands
from discord import app_commands

from extensions import config


class Guides(commands.Cog):

    '''Tag Commands'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='guide')
    @app_commands.describe(search='Term that u are looking for')
    async def guide(self, interaction: discord.Interaction, search: str):
        ''' 
        Will look through the guide channel and return those that contains what u need
        '''

        await interaction.response.defer()
        
        channel = interaction.guild.get_channel(config.dicas)

        em = discord.Embed(color=config.cinza,
                           description='')

        for thread in channel.threads:
            if search.lower() in thread.name.lower():
                em.description += f'[{thread.name}]({thread.jump_url})\n'

        async for thread in channel.archived_threads():
            if search.lower() in thread.name.lower():
                em.description += f'[{thread.name}]({thread.jump_url})\n'

        if em.description == '':
            em.description = f'Couldn\'t find anything related to {search}'
        else:
            em.title = 'Related guides'

        await interaction.edit_original_response(embed=em)


async def setup(bot: commands.Bot):
    await bot.add_cog(Guides(bot))
