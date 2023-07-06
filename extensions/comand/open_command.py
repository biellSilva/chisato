import discord
import datetime
import time

from discord import app_commands
from discord.ext import commands
from typing import Optional

from extensions import config
from extensions.utils import check_date_format


class Commands(commands.Cog):

    ''' Uncategorized Commands '''

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name='avatar')
    @app_commands.describe(member='Select a member', image='Select between Discord or Guild avatar, default: Guild')
    @app_commands.choices(
        image=[
            app_commands.Choice(name='Guild Avatar', value=0),
            app_commands.Choice(name='Discord Avatar', value=1)
            ])
    async def avatar(self, interaction: discord.Interaction, member: Optional[discord.Member], image: Optional[int] = 0):

        ''' Member Avatar '''

        member = member or interaction.user
        em = discord.Embed(color=config.cinza)
        
        if image == 0:
            em.set_image(url=member.display_avatar.url)
            em.set_footer(text=member.display_name,
                          icon_url=member.display_avatar.url)
        elif image == 1:
            em.set_image(url=member.avatar.url)
            em.set_footer(text=f'{member.name} | {member.global_name}',
                          icon_url=member.avatar.url)

        await interaction.response.send_message(embed=em)


    @commands.hybrid_command(name='unixtime', aliases=['unix', 'ut'], with_app_command=True)
    @app_commands.describe(date='dd/mm/yyyy', hour='HH:MM')
    async def unixtime(self, ctx: commands.Context, date: Optional[str], hour: Optional[str]):

        ''' Convert datetime to Discord timestamp '''

        if not date and not hour:
            unixtime = int(time.time())
        
        elif date and hour:
            unixtime = int(time.mktime(check_date_format(f'{date} {hour}')))

        else:
            unixtime = int(time.mktime(check_date_format(date)))

        em = discord.Embed(color=config.cinza,
                           title='Discord Timestamps',
                           description=f'''
                           \<t:{unixtime}> - <t:{unixtime}>
                           \<t:{unixtime}:t> - <t:{unixtime}:t>
                           \<t:{unixtime}:T> - <t:{unixtime}:T>
                           \<t:{unixtime}:d> - <t:{unixtime}:d>
                           \<t:{unixtime}:D> - <t:{unixtime}:D>
                           \<t:{unixtime}:f> - <t:{unixtime}:f>
                           \<t:{unixtime}:F> - <t:{unixtime}:F>
                           \<t:{unixtime}:R> - <t:{unixtime}:R>
                           ''')

        await ctx.send(embed=em, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))

