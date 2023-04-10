import discord

from discord import app_commands
from discord.ext import commands
from time import time

from extensions import config
from extensions.views.colors_view import ColorsView


class ColorsCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def colors(self, ctx: commands.Context, name: str, hex: str):
        '''Create role with hex color'''

        role = await ctx.guild.create_role(name=name, colour=int(hex.replace('#', ''), 16))
        
        await ctx.guild.edit_role_positions({role: len(ctx.guild.roles)-7})

        await ctx.send(role.mention)

    @app_commands.command(name='colors')
    @app_commands.checks.has_role(config.tof_member)
    async def embed_colors(self, interaction: discord.Interaction):
        '''Create a embed colors'''

        em=discord.Embed(color=config.cinza, title='Auto Color', description=f'Countdown: <t:{int(time())+180}:R>')
        em.set_footer(text='Choose your color')

        for color_id in config.colors_list:
            color = interaction.guild.get_role(color_id)
            em.description+=f'{color.mention}\n'

        await interaction.response.send_message(embed=em, ephemeral=True, view=ColorsView(timeout=180))


async def setup(bot):
    await bot.add_cog(ColorsCommand(bot))
