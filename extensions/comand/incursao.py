import discord
import time
import datetime

from discord import app_commands
from discord.ext import commands
from typing import Optional
from ast import literal_eval

from extensions import config
from extensions.views.incursao_view import IncursaoView
from extensions.views.groups_view import GroupsView


@app_commands.guild_only()
class Groups(commands.Cog):

    '''A Collection of commands related to in-game groups'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.incursao_view = IncursaoView(timeout=None)
        self.groups_view = GroupsView(timeout=None)
    
    async def cog_load(self):
        self.bot.add_view(self.incursao_view)
        self.bot.add_view(self.groups_view)

    group = app_commands.Group(name='group', description='Create your own group')

    raid = app_commands.Group(name='raid', description='Create your own group for ToF raids', parent=group)

    @group.command(name='create', description='Create your own group for in-game things')
    @app_commands.checks.has_role(config.tof_member)
    @app_commands.describe(event='Discord Role', data='ex.: dd/mm/yyyy HH:MM', level='Minimal level', slots='How many vacancies?', description='Extra information', color='hex color: #fcba03')
    async def group_create(self, interaction: discord.Interaction, event: discord.Role, data: str, level: Optional[int], slots: Optional[int], description: Optional[str], color: Optional[str]):
        '''Create your own in-game group'''

        await interaction.response.defer(ephemeral=True, thinking=True)

        guild = interaction.guild
        groups_channel = guild.get_channel(config.groups_channel)

        error_embed = discord.Embed(color=config.vermelho, description='',
                                    title='Error')
        
        if not event.mentionable or event.name.lower() in ('admin', 'staff', 'oficial'):
            error_embed.description = f'{event.mention} isn\'t a in-game role'
            await interaction.edit_original_response(embed=error_embed)
            return


        try:
            data = int(time.mktime(datetime.datetime.strptime(
                data, '%d/%m/%Y %H:%M').timetuple()))
        except:
            try:
                data = int(time.mktime(datetime.datetime.strptime(
                    f'{datetime.date.today()} {data}', '%Y-%m-%d %H:%M').timetuple()))
            except:
                try:
                    data = int(time.mktime(datetime.datetime.strptime(
                        f'{data} 21:00', '%d/%m/%Y %H:%M').timetuple()))
                except:
                    error_embed.description = (f'Invalid datetime format:\n'
                                               '**Expected:**\n'
                                               '`22/12/2022 21:00`\n'
                                               '`21:00`\n'
                                               '`22/12/2022`\n\n'
                                               f'**Received:** {data}')

                    await interaction.edit_original_response(embed=error_embed)
                    return

        if color:
            if len(color) == len('#20B2AA'):
                try:
                    color = literal_eval(color.replace(
                        ' ', '').replace('#', '0x'))
                except:
                    error_embed.description = ('**Invalid HEX:**\n'
                                               f'**Expected:** #20B2AA\n'
                                               f'**Received:** {color}')
                    await interaction.edit_original_response(embed=error_embed)
                    return
            else:
                error_embed.description = ('**Invalid HEX:**\n'
                                           f'**Expected:** #20B2AA | Lenght: {len("#20B2AA")}\n'
                                           f'**Received:** {color} | Lenght: {len(color)}')
                await interaction.edit_original_response(embed=error_embed)
                return
        else:
            color = config.cinza

        em = discord.Embed(title=f'{event.name} {"" if level is None else f"[lvl: {level}]"}',
                           color=color,
                           description=f'*Group start: <t:{data}:F>, <t:{data}:R>*\n\n'
                                       f'{"" if description is None else f"Description: **{description}**"}',
                           timestamp=datetime.datetime.fromtimestamp(data))
        
        em.set_footer(text=f'{interaction.user.display_name} - {interaction.user.id}', icon_url=interaction.user.display_avatar)

        em.add_field(name='Members', value='\u200B')
        if slots:
            em.add_field(name='Vacancies', value=slots)

        await interaction.edit_original_response(content=f'Done! {groups_channel.mention}')
        return await groups_channel.send(content=event.mention, embed=em, view=GroupsView())


    @raid.command(name='unofficial', description='Create your own group for ToF raids')
    @app_commands.describe(data='ex.: dd/mm/yyyy HH:MM', level='minimal level', description='Bosses', color='hex color: #fcba03')
    async def raids(self, interaction: discord.Interaction, level: int, data: str, description: str, color: Optional[str]):

        '''Create your own group for ToF raids'''

        await interaction.response.defer(ephemeral=True, thinking=True)

        guild = interaction.guild
        groups_channel = guild.get_channel(config.groups_channel)
        incursao_role = guild.get_role(config.raid)

        error_embed = discord.Embed(color=config.vermelho, description='',
                                    title='Error')

        try:
            data = int(time.mktime(datetime.datetime.strptime(
                data, '%d/%m/%Y %H:%M').timetuple()))
        except:
            try:
                data = int(time.mktime(datetime.datetime.strptime(
                    f'{datetime.date.today()} {data}', '%Y-%m-%d %H:%M').timetuple()))
            except:
                try:
                    data = int(time.mktime(datetime.datetime.strptime(
                        f'{data} 21:00', '%d/%m/%Y %H:%M').timetuple()))
                except:
                    error_embed.description = (f'Invalid datetime format:\n'
                                            '**Expected:**\n'
                                            '`22/12/2022 21:00`\n'
                                            '`21:00`\n'
                                            '`22/12/2022`\n\n'
                                            f'**Received:** {data}')

                    await interaction.edit_original_response(embed=error_embed)
                    return

        if color:
            if len(color) == len('#20B2AA'):
                try:
                    color = literal_eval(color.replace(
                        ' ', '').replace('#', '0x'))
                except:
                    error_embed.description = ('**Invalid HEX:**\n'
                                            f'**Expected:** #20B2AA\n'
                                            f'**Received:** {color}')
                    await interaction.edit_original_response(embed=error_embed)
                    return
            else:
                error_embed.description = ('**Invalid HEX:**\n'
                                        f'**Expected:** #20B2AA | Lenght: {len("#20B2AA")}\n'
                                        f'**Received:** {color} | Lenght: {len(color)}')
                await interaction.edit_original_response(embed=error_embed)
                return
        else:
            color = config.cinza

        em = discord.Embed(title=f'Raid [lvl: {level}]',
                        color=color,
                        description=f'''
                        *Raid start: <t:{data}:F>, <t:{data}:R>*
                        *Group start: <t:{data - 300}:F>, <t:{data - 300}:R>*

                        Bosses: **{description}**
                        ''')

        em.add_field(name='DPS', value='\u200B')
        em.add_field(name='SUP', value='\u200B')
        em.add_field(name='TANK', value='\u200B')
        em.add_field(name='RESERVE', value='\u200B')

        em1 = discord.Embed(color=color)
        em1.add_field(name='DPS Slots:', value=5)
        em1.add_field(name='SUP Slots:', value=2)
        em1.add_field(name='TANK Slots:', value=1)

        await interaction.edit_original_response(content=f'Done! {groups_channel.mention}')
        await groups_channel.send(content=incursao_role.mention, embeds=[em, em1], view=IncursaoView())


    @raid.command(name='official')
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(data='ex.: dd/mm/yyyy HH:MM', level='minimal level', description='Bosses', color='hex color: #fcba03')
    @app_commands.choices(
        groups=[
            app_commands.Choice(name='8 Members / 1 Group', value='8'),
            app_commands.Choice(name='16 Members / 2 Groups', value='16'),
            app_commands.Choice(name='24 Members / 3 Groups', value='24')])
    async def oficial(self, interaction: discord.Interaction, level: int, data: str, description: str, groups: str, color: Optional[str]):

        '''Create a official group for ToF raids'''

        await interaction.response.defer(ephemeral=True, thinking=True)

        guild = interaction.guild
        incursao_channel = guild.get_channel(config.incursao_channel)
        incursao_role = guild.get_role(config.raid)

        error_embed = discord.Embed(color=config.vermelho, description='',
                            title='Error')

        try:
            data = int(time.mktime(datetime.datetime.strptime(
                data, '%d/%m/%Y %H:%M').timetuple()))
        except:
            try:
                data = int(time.mktime(datetime.datetime.strptime(
                    f'{datetime.date.today()} {data}', '%Y-%m-%d %H:%M').timetuple()))
            except:
                try:
                    data = int(time.mktime(datetime.datetime.strptime(
                        f'{data} 21:00', '%d/%m/%Y %H:%M').timetuple()))
                except:
                    error_embed.description = (f'Invalid datetime format:\n'
                                               '**Expected:**\n'
                                               '`22/12/2022 21:00`\n'
                                               '`21:00`\n'
                                               '`22/12/2022`\n\n'
                                               f'**Received:** {data}')

                    await interaction.edit_original_response(embed=error_embed)
                    return

        if color:
            if len(color) == len('#20B2AA'):
                try:
                    color = literal_eval(color.replace(' ', '').replace('#', '0x'))
                except:
                    error_embed.description = ('**Invalid HEX:**\n'
                                               f'**Expected:** #20B2AA\n'
                                               f'**Received:** {color}')
                    await interaction.edit_original_response(embed=error_embed)
                    return
            else:
                error_embed.description = ('**Invalid HEX:**\n'
                                           f'**Expected:** #20B2AA | Lenght: {len("#20B2AA")}\n'
                                           f'**Received:** {color} | Lenght: {len(color)}')
                await interaction.edit_original_response(embed=error_embed)
                return
        else:
            color = config.cinza

        em = discord.Embed(title=f'Oficial Raid [lvl: {level}]',
                           color=color,
                           description=f'''
                           *Raid start: <t:{data}:F>, <t:{data}:R>*
                           *Group start: <t:{data - 300}:F>, <t:{data - 300}:R>*

                           Bosses: **{description}**

                           The members below will be listed and reassigned to the respective groups in a balanced way having their groups formed and posted on the day of the raid
                           ''')

        em.add_field(name='DPS', value='\u200B')
        em.add_field(name='SUP', value='\u200B')
        em.add_field(name='TANK', value='\u200B')
        em.add_field(name='RESERVE', value='\u200B')

        em1 = discord.Embed(color=color)
        
        if groups:
            if groups == '8':
                em1.add_field(name='DPS Slots:', value=5)
                em1.add_field(name='SUP Slots:', value=2)
                em1.add_field(name='TANK Slots:', value=1)

            elif groups == '16':
                em1.add_field(name='DPS Slots:', value=10)
                em1.add_field(name='SUP Slots:', value=4)
                em1.add_field(name='TANK Slots:', value=2)

            elif groups == '24':
                em1.add_field(name='DPS Slots:', value=14)
                em1.add_field(name='SUP Slots:', value=6)
                em1.add_field(name='TANK Slots:', value=4)


        await interaction.edit_original_response(content=f'Done! {incursao_channel.mention}')
        await incursao_channel.send(content= incursao_role.mention, embeds=[em, em1], view=IncursaoView())

    
async def setup(bot):
    await bot.add_cog(Groups(bot))

