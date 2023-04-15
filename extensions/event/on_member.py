import discord

from discord.ext import commands
from datetime import datetime

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
        welcome_channel = guild.get_channel(config.member_log)

        em = discord.Embed(color=config.cinza, title='Member Joined',
                           description=f'{member.mention} joined us',
                           timestamp=datetime.now(config.tz_brazil))
        em.set_footer(text=f'{member} - {member.id}', icon_url=member.display_avatar.url)

        await welcome_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_raw_member_remove(self, member: discord.Member):

        ''' Member left the guild '''

        if member.bot:
            return

        guild = self.bot.get_guild(config.henko)
        welcome_channel = guild.get_channel(config.member_log)

        em = discord.Embed(color=config.cinza, title='Member Leave',
                           description=f'{member.name}#{member.discriminator} leaved us',
                           timestamp=datetime.now(config.tz_brazil))

        await welcome_channel.send(embed=em)

async def setup(bot):
    await bot.add_cog(On_member(bot))
