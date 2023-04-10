import discord

from discord.ext import commands
from datetime import datetime

from extensions import config


class Suggestion(commands.Cog):

    '''On Message Suggestion's Listener'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        ''' Suggestions Channel '''

        if message.author.bot:
            return
        
        em = discord.Embed(color=config.cinza, description='')

        if message.channel.id == config.guild_name_suggest:
            em.title='Guild Name Suggestion'
            em.description=message.content
            em.timestamp=datetime.now(tz=config.tz_brazil)

            em.set_footer(text=f'{message.author.display_name} - {message.author.id}', icon_url=message.author.display_avatar.url)

            if message.attachments:
                em.set_image(url=message.attachments[0].url)

            msg = await message.channel.send(embed=em)
            await message.delete()
            await msg.add_reaction(config.like)
            return
        
        if message.channel.id == config.discord_suggest:
            em.title = 'Discord Suggestion'
            em.description = message.content
            em.timestamp = datetime.now(tz=config.tz_brazil)

            em.set_footer(text=f'{message.author.display_name} - {message.author.id}',
                          icon_url=message.author.display_avatar.url)

            if message.attachments:
                em.set_image(url=message.attachments[0].url)

            msg = await message.channel.send(embed=em)
            await message.delete()
            await msg.add_reaction(config.like)
            await msg.add_reaction(config.dislike)
            return


async def setup(bot):
    await bot.add_cog(Suggestion(bot))
