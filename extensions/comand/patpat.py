import discord

from discord import app_commands
from discord.ext import commands
from typing import Optional, Union

from ..PatPatCreator import PatPatCreator


class PatPatCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='patpat', description='Faz carinho em alguem ou algo')
    @app_commands.describe(user='Discord user', file='Arquivo de imagem')
    async def patpat_command(self, ctx: commands.Context[commands.Bot], user: Optional[Union[discord.Member, discord.User]], file: Optional[discord.Attachment]):
        if ctx.interaction:
            await ctx.interaction.response.defer()

        if user and file:
            return ctx.reply('Apenas 1 item')
        
        if user:
            url = user.display_avatar.url
        elif file:
            url = file.proxy_url
        else:
            url = ctx.author.display_avatar.url

        patpat_buffer = await PatPatCreator(image_url=url).create_gif()
        patpat_gif = discord.File(patpat_buffer, filename='patpat.gif')

        await ctx.send(file=patpat_gif)



async def setup(bot: commands.Bot):
    await bot.add_cog(PatPatCog(bot))