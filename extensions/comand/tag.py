import discord

from discord.ext import commands
from discord import app_commands

from extensions import config


class Tag(commands.Cog):

    '''Tag Commands'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='tag')
    async def tag(self, interaction: discord.Interaction, search: str):
        ''' 
        Tag command will look through all channels and 
        return those that contains your variable on the title 
        '''
        await interaction.response.defer()
        
        channel = interaction.guild.get_channel(config.dicas)

        em = discord.Embed(color=config.cinza,
                           description='')

        for thread in channel.threads:
            if search.lower() in thread.name.lower():
                em.description += f'{thread.jump_url}\n'

        async for thread in channel.archived_threads():
            if search.lower() in thread.name.lower():
                em.description += f'{thread.jump_url}\n'

        if em.description == '':
            em.description = f'Couldn\'t find anything related to {search}'
        else:
            em.title = 'Related channel\'s'

        await interaction.edit_original_response(embed=em)


async def setup(bot):
    await bot.add_cog(Tag(bot))
