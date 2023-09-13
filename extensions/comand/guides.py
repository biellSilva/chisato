import discord

from discord.ext import commands
from discord import app_commands

from extensions import config


class Guides(commands.Cog):

    '''Tag Commands'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='guides', aliases=['guias', 'guia'])
    @app_commands.describe(search='Term that u are looking for')
    async def guide(self, ctx: commands.Context, search: str):
        ''' 
        Will look through the guide channel and return those that contains what u need
        '''

        if ctx.interaction:
            await ctx.interaction.response.defer()
        
        channel = ctx.guild.get_channel(config.dicas)

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

        await ctx.reply(embed=em)


async def setup(bot: commands.Bot):
    await bot.add_cog(Guides(bot))
