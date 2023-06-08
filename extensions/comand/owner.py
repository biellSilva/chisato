from typing import Optional
from discord.ext import commands


class Owner(commands.Cog):

    '''Owner Commands'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='sync')
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, spec: Optional[str]):
        async with ctx.typing():
            if spec:
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                sync = []
            else:
                sync = await ctx.bot.tree.sync()
                
            await ctx.reply(f'{len(sync)} commands synced')


async def setup(bot):
    await bot.add_cog(Owner(bot))
