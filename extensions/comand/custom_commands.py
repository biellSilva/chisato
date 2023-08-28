import discord
import json

from discord import app_commands
from discord.ext import commands
from typing import Optional
from os import path, makedirs


class CustomCommandsCog(commands.GroupCog, group_name='commands', group_description='Adicione comandos que são chamados via prefix [ c! ]'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        if not path.exists('./extensions/assets/custom_commands'):
            makedirs('./extensions/assets/custom_commands')

        if not path.exists('./extensions/database'):
            makedirs('./extensions/database')
            with open('./extensions/database/CustomCommands.json', 'w') as f:
                data = json.dumps({}, indent=2)
                f.write(data)

        with open('./extensions/database/CustomCommands.json', 'rb') as f:
            try:
                self.data: dict = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                self.data = {}


    @app_commands.command(name='add')
    async def add_command(self, interaction: discord.Interaction, name: str, content: Optional[str], file: Optional[discord.Attachment]):
        await interaction.response.defer(ephemeral=True)

        if name.lower() in self.data:
            await interaction.edit_original_response(content=f'{name.lower()} já existe como comando')

        else:
            if file:
                with open(f'./extensions/assets/custom_commands/{interaction.user.id}_{name.lower()}.{file.content_type.split("/")[1]}', 'wb') as f:
                    f.write(await file.read())

            self.data.update({
                name.lower() : {
                    'name': name,
                    'content': content,
                    'file': None if not file else f'{interaction.user.id}_{name.lower()}.{file.content_type.split("/")[1]}',
                    'file_format': None if not file else {file.content_type.split("/")[1]},
                    'author': interaction.user.name,
                    'author_id': str(interaction.user.id)
                }
            })

            with open('./extensions/database/CustomCommands.json', 'w') as f:
                data = json.dumps(obj=self.data, indent=2)
                f.write(data)
        
            await interaction.edit_original_response(content=f'c!{name.lower()}')

    
    @commands.Cog.listener(name='on_message')
    async def custom_command_response(self, message: discord.Message):
        if message.author.bot:
            return
        
        if message.content and message.content.startswith('c!'):
            command = message.content.split('c!', 1)[1]
            if command.lower() in self.data:
                data = self.data[command.lower()]
                
                if data['file']:
                    file = open(f'./extensions/assets/custom_commands/{data["author_id"]}_{data["name"].lower()}.{data["file_format"]}')
                else:
                    file = None

                await message.reply(content=data["content"], file=file)


async def setup(bot: commands.Bot):
    await bot.add_cog(CustomCommandsCog(bot))