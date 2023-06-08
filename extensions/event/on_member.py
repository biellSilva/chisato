import discord

from discord.ext import commands

from extensions import config


class On_member(commands.Cog):

    '''On Member Listeners'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        ''' Member joined the guild '''

        if member.bot:
            return

        guild = self.bot.get_guild(config.henko)
        welcome_channel = guild.get_channel(config.welcome)
        ptRules = guild.get_channel(config.ptRules)
        enRules = guild.get_channel(config.esRules)

        em = discord.Embed(color=config.cinza, title=f'Welcome to {guild.name}',
                           description=(f'Please make sure to read our rules channel\'s {ptRules.mention} or {enRules.mention},' 
                           'for everything you need to know about our server, and gain access to our chats once you are ready!'))
        
        em.set_footer(text=f'{guild.member_count} members', icon_url=guild.icon.url)
        em.set_image(url='https://media.tenor.com/lfYGrPJlQLAAAAAd/oshi-no-ko-ruby.gif')

        await welcome_channel.send(content={member.mention}, embed=em)

async def setup(bot):
    await bot.add_cog(On_member(bot))
