import discord

from discord import app_commands
from discord.ext import commands
from typing import Optional

from extensions import config


class AdminCommands(commands.Cog):

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
            roles = [role.mention for role in member.roles]
            em.add_field(name='Roles', value=roles)
        
        await interaction.response.send_message(embed=em, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
