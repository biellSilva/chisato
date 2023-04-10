from discord import app_commands
from discord.ext import commands


class HelpCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='help')
    async def help_command(self, ctx: commands.Context):
        '''Help Command'''

        await ctx.send_help()


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
