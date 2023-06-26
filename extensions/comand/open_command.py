import discord
import datetime
import time

from discord import app_commands
from discord.ext import commands
from typing import Optional

from extensions import config


class Commands(commands.Cog):

    '''Uncategorized Commands'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name='avatar')
    @app_commands.describe(member='Select a member', image='Select between discord or guild avatar')
    @app_commands.choices(
        image=[
            app_commands.Choice(name='Guild Avatar', value=0),
            app_commands.Choice(name='Discord Avatar', value=1)
            ])
    async def avatar(self, interaction: discord.Interaction, member: Optional[discord.Member], image: Optional[int] = 0):

        ''' Member Avatar or Banner'''

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
        else:
            em.description=f'Argument `image` can\'t be {image}'

        await interaction.response.send_message(embed=em)


    @commands.hybrid_command(name='unixtime', aliases=['unix', 'ut'], with_app_command=True)
    @app_commands.describe(date='dd/mm/yyyy', hour='HH:MM')
    async def unixtime(self, ctx: commands.Context, date: Optional[str], hour: Optional[str]):

        ''' Convert datetime to Discord timestamp '''

        if not date and not hour:
            unixtime = int(time.time())
        
        elif date and hour:
            unixtime = int(time.mktime(datetime.datetime.strptime(f'{date} {hour}', '%d/%m/%Y %H:%M').timetuple()))

        else:
            try:
                unixtime = int(time.mktime(datetime.datetime.strptime(f'{date} 21:00', '%d/%m/%Y %H:%M').timetuple()))
            except:
                if not hour and not ctx.interaction:
                    hour = date
                unixtime = int(time.mktime(datetime.datetime.strptime(f'{datetime.date.today()} {hour}', '%Y-%m-%d %H:%M').timetuple()))


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


async def setup(bot):
    await bot.add_cog(Commands(bot))







'''

amanha entrevista, as 16 horas

'''