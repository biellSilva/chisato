import discord

from discord.ext import commands
from discord import app_commands

from extensions import config


class RandomContextMenus(commands.Cog):

    '''Random Context Menus'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.add_emote = app_commands.ContextMenu(name='Add Emote', callback=self.add_emote_menu)

    async def cog_load(self):
        self.bot.tree.add_command(self.add_emote)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.add_emote.name, type=self.add_emote.type)
    
    
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add_emote_menu(self, interaction: discord.Interaction, message: discord.Message):
        
        ''' Add emotes from message to the guild '''

        await interaction.response.defer()

        names: list = message.content.split()

        for name, emoji in zip(names, message.attachments):
            try:
                added_emote = await interaction.guild.create_custom_emoji(name=name, image=await emoji.read())
                await interaction.edit_original_response(content=added_emote)
            except discord.HTTPException as err:
                if err.code == 30008:
                    await interaction.edit_original_response(content=err.text)

async def setup(bot: commands.Bot):
    await bot.add_cog(RandomContextMenus(bot))
