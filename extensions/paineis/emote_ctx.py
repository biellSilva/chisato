import discord

from discord.ext import commands
from discord import app_commands

from extensions import config


class RandomContextMenus(commands.Cog):

    '''Random Context Menus'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        self.add_emote = app_commands.ContextMenu(
            name='Add Emote',
            callback=self.add_emote_menu
        )

    async def cog_load(self):
        self.bot.tree.add_command(self.add_emote)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.add_emote.name, type=self.add_emote.type)
    

    @app_commands.checks.has_permissions(manage_messages=True)
    async def add_emote_menu(self, interaction: discord.Interaction, message: discord.Message):
        
        ''' Add emotes from message to the guild '''

        await interaction.response.defer()

        em = discord.Embed(color=config.cinza, title='Add Emote', description='')
        names: list = message.content.split()

        for name, emoji in zip(names, message.attachments):
            added_emote = await interaction.guild.create_custom_emoji(name=name, image=await emoji.read())
            em.add_field(name=added_emote.name, value=added_emote)

        await interaction.edit_original_response(embed=em)
        
    
async def setup(bot):
    await bot.add_cog(RandomContextMenus(bot))
