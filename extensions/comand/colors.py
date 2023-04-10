import discord

from discord import app_commands
from discord.ext import commands

from extensions import config
from extensions.views.colors_view import ColorsView


class ColorsCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.colors_view = ColorsView(timeout=None)

    async def cog_load(self):
        self.bot.add_view(self.colors_view)
        

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def colors(self, ctx: commands.Context, name: str, hex: str):
        '''Create role with hex color'''

        if not ctx.author.guild_permissions.kick_members:
            await ctx.reply('Missing permission')
            return

        role = await ctx.guild.create_role(name=name, colour=int(hex.replace('#', ''), 16))
        
        await ctx.guild.edit_role_positions({role: len(ctx.guild.roles)-7})

        await ctx.send(role.mention)

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def embed_colors(self, ctx: commands.Context):
        '''Create a embed colors'''

        em=discord.Embed(color=config.cinza, title='Auto Color', description='')
        em.set_footer(text='Choose your color')

        colors = config.colors_list

        for color_id in colors:
            color = ctx.guild.get_role(color_id)
            em.description+=f'{color.mention} - {color.color}\n'

        await ctx.send(embed=em)


async def setup(bot):
    await bot.add_cog(ColorsCommand(bot))
