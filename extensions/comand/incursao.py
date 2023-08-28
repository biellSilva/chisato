import discord
import time
import datetime

from discord import app_commands
from discord.ext import commands
from typing import Optional

from extensions import config
from extensions.utils import check_date_format, check_color_hex, NotMentionableRole
from extensions.views.incursao_view import IncursaoView
from extensions.views.groups_view import GroupsView


class Groups(commands.Cog):

    '''A Collection of commands related to in-game groups'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.incursao_view = IncursaoView(timeout=None)
        self.groups_view = GroupsView(timeout=None)
    
    async def cog_load(self):
        self.bot.add_view(self.incursao_view)
        self.bot.add_view(self.groups_view)

    create = app_commands.Group(name='create', description='Main group command for in-game teams', guild_only=True)

    @create.command(name='team', description='Create your own in-game team')
    @app_commands.checks.has_role(config.tof_member)
    @app_commands.describe(event='Mentionable Discord Role', 
                           date='dd/mm/yyyy HH:MM utc-3', 
                           level='Minimal level', 
                           slots='How many vacancies?', 
                           description='Extra information', 
                           color='HEX color: #fcba03')
    async def group_create(self, interaction: discord.Interaction, 
                           event: discord.Role, date: str, 
                           level: Optional[int], slots: Optional[int], description: Optional[str], color: Optional[str]):
        
        '''Create your in-game team'''

        await interaction.response.defer(ephemeral=True, thinking=True)

        guild = interaction.guild
        groups_channel = guild.get_channel(config.groups_channel)

        if not event.mentionable:
            raise NotMentionableRole(event)

        date = int(time.mktime(check_date_format(date)))

        if color:
            color = check_color_hex(color)
        else:
            color = config.cinza

        em = discord.Embed(title=f'{event.name}',
                           color=color,
                           description=f'*Starts **<t:{date}:R>**, **<t:{date}:F>***\n'
                                       f'**(the time is automatically converted to your local timezone)**',
                           timestamp=datetime.datetime.fromtimestamp(date))
        
        if level:
            em.title += f' [lvl: {level}]'

        if description:
            em.description += f'\n\n**{description}**'
        
        em.set_footer(text=f'{interaction.user.name} - {interaction.user.id}', icon_url=interaction.user.display_avatar)

        em.add_field(name='Members', value='\u200B')

        if slots:
            em.add_field(name='Vacancies', value=slots)

        await interaction.edit_original_response(content=f'Done! {groups_channel.mention}')
        await groups_channel.send(content=event.mention, embed=em, view=GroupsView())


    
    @create.command(name='raid')
    @app_commands.describe(date='dd/mm/yyyy HH:MM utc-3', level='Minimal level', 
                           description='Extra info', color='HEX color: #fcba03', 
                           groups='How many groups?')
    @app_commands.choices(
        groups=[
            app_commands.Choice(name='8 Members / 1 Group', value='8'),
            app_commands.Choice(name='16 Members / 2 Groups', value='16'),
            app_commands.Choice(name='24 Members / 3 Groups', value='24')])
    async def raid(self, interaction: discord.Interaction, 
                      date: str, groups: Optional[str], 
                      level: Optional[int], description: Optional[str], 
                      color: Optional[str]):

        '''Create your in-game team for raids'''

        await interaction.response.defer(ephemeral=True, thinking=True)

        guild = interaction.guild
        incursao_channel = guild.get_channel(config.incursao_channel)
        incursao_role = guild.get_role(config.raid)

        date = int(time.mktime(check_date_format(date)))

        if color:
            color = check_color_hex(color)
        else:
            color = config.cinza

        em = discord.Embed(title=f'{incursao_role.name}',
                           color=color,
                           description=f'Starts **<t:{date}:R>**, **<t:{date}:F>**\n'
                                       f'*(the time is automatically converted to your local timezone)*',
                           timestamp=datetime.datetime.fromtimestamp(date))
        
        if level:
            em.title += f' [lvl: {level}]'

        if description:
            em.description += f'\n\n**{description}**'
        
        em.set_footer(text=f'{interaction.user.name} - {interaction.user.id}', icon_url=interaction.user.display_avatar)

        em.add_field(name='DPS', value='\u200B')
        em.add_field(name='SUP', value='\u200B')
        em.add_field(name='TANK', value='\u200B')
        em.add_field(name='RESERVE', value='\u200B')

        em1 = discord.Embed(color=color)

        if not groups:
            em1.add_field(name='DPS Slots:', value=5)
            em1.add_field(name='SUP Slots:', value=2)
            em1.add_field(name='TANK Slots:', value=1)
        
        elif groups and interaction.user.guild_permissions.kick_members:
            if groups == '8':
                em1.add_field(name='DPS Slots:', value=5)
                em1.add_field(name='SUP Slots:', value=2)
                em1.add_field(name='TANK Slots:', value=1)

            elif groups == '16':
                em1.add_field(name='DPS Slots:', value=10)
                em1.add_field(name='SUP Slots:', value=4)
                em1.add_field(name='TANK Slots:', value=2)
                em.description += f'\n\n*The members below will be listed and reassigned to the respective groups in a balanced way having their groups formed and posted on the day of the raid*'

            elif groups == '24':
                em1.add_field(name='DPS Slots:', value=14)
                em1.add_field(name='SUP Slots:', value=6)
                em1.add_field(name='TANK Slots:', value=4)
                em.description += f'\n\n*The members below will be listed and reassigned to the respective groups in a balanced way having their groups formed and posted on the day of the raid*'
        
        elif not interaction.user.guild_permissions.kick_members:
            em1.add_field(name='DPS Slots:', value=5)
            em1.add_field(name='SUP Slots:', value=2)
            em1.add_field(name='TANK Slots:', value=1)
            await interaction.followup.send(embed=discord.Embed(color=config.cinza, 
                                                                description='Changed group size to **8** since you don\'t have permission to **Kick Members**'),
                                            ephemeral=True)


        await interaction.edit_original_response(content=f'Done! {incursao_channel.mention}')
        await incursao_channel.send(content= incursao_role.mention, embeds=[em, em1], view=IncursaoView())

    
async def setup(bot: commands.Bot):
    await bot.add_cog(Groups(bot))

