import discord

from discord import app_commands
from discord.ext import commands
from typing import Optional

from extensions import config


class Admin(commands.Cog):

    '''Admin Commands'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    admin = app_commands.Group(name='admin', description='Admin commands', guild_only=True)

    user = app_commands.Group(name='users', description='Users related commands', parent=admin, guild_only=True)

    @user.command(name='check', description='Check the user parameters')
    @app_commands.checks.has_permissions(kick_members=True)
    async def check_user(self, interaction: discord.Interaction, member: Optional[discord.Member]):

        '''Check the member'''
        
        member = member or interaction.user

        em = discord.Embed(color=config.cinza, title=member,
                           description=f'''
                           ID: {member.id}
                           Display Name: {member.display_name}
                           Bot: {member.bot}
                           Status: {member.status}
                           Activity: {member.activity}
                           Color: {member.color}
                           Timed Out: {member.is_timed_out() if member.is_timed_out() is False else member.timed_out_until}
                           Discord Member Since: <t:{int(member.created_at.timestamp())}:f>
                           Guild Member Since: {"None" if member.joined_at is None else f"<t:{int(member.joined_at.timestamp())}:f>"}
                           Premium Since: {"None" if member.premium_since is None else f"<t:{int(member.premium_since.timestamp())}:f>"}
                           ''')
        em.set_thumbnail(url=member.display_avatar.url)
        if member.banner:
            em.set_image(url=member.banner.url)
        
        if member.roles:
            roles = ''
            for role in member.roles:
                if not role.is_default():
                    roles +=f'\n{role.mention}'

            em.add_field(name='Roles', value=roles)
        
        await interaction.response.send_message(embed=em, ephemeral=True)


    @admin.command(name='clean', description='Delete all messages from this channel')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clean_channel(self, interaction: discord.Interaction, user: Optional[discord.Member], limit: int = 100, ):
        '''Clean the channel'''

        await interaction.response.defer(thinking=True, ephemeral=True)

        def check(message: discord.Message):
            return message.author == user and message.channel == interaction.channel

        if user:
            await interaction.channel.purge(limit=limit, check=check, reason=f'{interaction.user} deleted')
        else:
            await interaction.channel.purge(limit=limit, reason=f'{interaction.user} deleted')

        await interaction.edit_original_response(content='Done!')
    
    @admin.commmand(name='role')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def role_comand(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(1116380664367951883)
        await role._move(4)

        await interaction.response.send_message('feito')

async def setup(bot):
    await bot.add_cog(Admin(bot))
