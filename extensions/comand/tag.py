from discord.ext import commands


class Tag(commands.Cog):

    '''Tag Commands'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='tag')
    async def tag(self, ctx: commands.Context, search: str):
        ''' 
        Tag command will look through all channels and 
        return those that contains your variable on the title 
        '''

        if ctx.interaction:
            await ctx.interaction.response.defer()
        
        channel = ctx.guild.get_channel(1093316378691387473)
        await ctx.send(channel.name)
        print(channel)

async def setup(bot):
    await bot.add_cog(Tag(bot))
