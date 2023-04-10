
from discord import Embed, HTTPException
from discord.ext import commands
from traceback import print_exception
from sys import stderr

from extensions import config
from extensions.bgcolors import bcolors


class CtxErrorHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, err):
        
        em = Embed(color=config.cinza,
                           description='')
        
        ignore = commands.CommandNotFound
        err = getattr(err, 'original', err)

        if isinstance(err, ignore):
            return
        
        if isinstance(err, commands.DisabledCommand):
            em.description = f'{ctx.command} command is disabled'
            return await ctx.send(embed=em)
        
        if isinstance(err, commands.NotOwner):
            em.description = 'You are not my owner'
            return await ctx.send(embed=em)
        
        if isinstance(err, commands.NoPrivateMessage):
            try:
                em.description = f'{ctx.command} command don\'t work on private messages'
                return await ctx.author.send(embed=em)
            except HTTPException:
                pass

        if isinstance(err, commands.MissingRequiredArgument):
            em.description = 'Missing argument'
            return await ctx.send(embed=em)

        if isinstance(err, IndexError):
            em.description = 'Couldn\'t find'
            await ctx.send(embed=em)

        if isinstance(err, commands.MissingPermissions):
            em.description = f'Missing permission'
            return await ctx.send(embed=em)

        print(f'\n{bcolors.WARNING}{"! ! "*30}\n'
              f'{bcolors.FAIL}{ctx.command} exception: ', file=stderr)
        print_exception(type(err), err, err.__traceback__, file=stderr)
        print(bcolors.ENDC)

async def setup(bot):
    await bot.add_cog(CtxErrorHandler(bot))
