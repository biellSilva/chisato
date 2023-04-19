import discord
import re

from discord.ext import commands
from discord import app_commands

from extensions import config


class Raids_Context(commands.Cog):

    '''Raids Context Menus'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        self.lista_menu = app_commands.ContextMenu(
            name='List Members',
            callback=self.listagem
        )
        self.membro_menu = app_commands.ContextMenu(
            name='Add Member',
            callback=self.adicionar_membro
        )
        self.membro_menu_2 = app_commands.ContextMenu(
            name='Remove Member',
            callback=self.remover_membro
        )

        self.bot.tree.add_command(self.lista_menu)
        self.bot.tree.add_command(self.membro_menu)
        self.bot.tree.add_command(self.membro_menu_2)

    async def cog_unload(self):
        self.bot.tree.remove_command(
            self.lista_menu.name, type=self.lista_menu.type)
        self.bot.tree.remove_command(
            self.membro_menu.name, type=self.membro_menu.type)
        self.bot.tree.remove_command(
            self.membro_menu_2.name, type=self.membro_menu_2.type)
        

    async def listagem(self, interaction: discord.Interaction, message: discord.Message):
        '''Listagem dos campos da embed'''

        await interaction.response.defer(thinking=True, ephemeral=True)

        msg = ''

        for field in message.embeds[0].fields:
            msg += f'\n\n**{field.name}**'

            for member in list(filter(None, field.value.replace('\u200B', '').split('\n'))):
                new_member = interaction.guild.get_member(int(re.sub(r'[^0-9]', '', member)))
                msg += f'\n{new_member.display_name}'

        await interaction.edit_original_response(content=msg)
        return

    async def adicionar_membro(self, interaction: discord.Interaction, message: discord.Message):

        '''Add a member to the raid'''

        await interaction.response.defer(ephemeral=True, thinking=True)

        embed = message.embeds

        em = discord.Embed(color=config.cinza, description='')

        if not interaction.user.guild_permissions.kick_members:
            em.description = 'You do not have permissions for this'
            await interaction.edit_original_response(embed=em)
            return

        em.description = f'Inform a member and his function\nex.: @biell dps'
        await interaction.edit_original_response(embed=em)

        def check(response: discord.Message):
            return response.author == interaction.user and response.channel == interaction.channel

        response: discord.Message = await self.bot.wait_for('message', check=check)

        try:
            membro = response.mentions[0]
        except:
            em.description=f'A member mention is needed'
            await interaction.edit_original_response(embed=em)
            return await response.delete()
        
        cargo = response.content.split(' ')[1]

        if cargo not in ('dps', 'sup', 'tank'):
            em.description=f'{cargo} is not accepted\nExpected: `DPS`, `SUP`, `TANK`'
            await interaction.edit_original_response(embed=em)
            return await response.delete()

        for field in embed[0].fields:
            if membro.mention in field.value:
                em.description = f'**{membro.mention}** already in **{field.name}**'
                await interaction.edit_original_response(embed=em)
                await response.delete()
                return

        for field in embed[0].fields:
            if cargo.lower() in field.name.lower():
                if 'dps' in field.name.lower():
                    ind = 0
                if 'sup' in field.name.lower():
                    ind = 1
                if 'tank' in field.name.lower():
                    ind = 2

                if int(embed[1].fields[ind].value) <= 0:
                    em.description = f'**{field.name}** is full'
                    return await interaction.edit_original_response(embed=em)

                embed[0].set_field_at(ind, name=field.name, value=field.value+f'\n{membro.mention}')
                embed[1].set_field_at(ind, name=embed[1].fields[ind].name, value=int(embed[1].fields[ind].value)-1)

                await message.edit(embeds=embed)
                em.description = f'**{membro}** added to **{field.name}**'
                await interaction.edit_original_response(embed=em)
                await response.delete()
                return

    async def remover_membro(self, interaction: discord.Interaction, message: discord.Message):
        '''Remover o Membro'''

        await interaction.response.defer(ephemeral=True, thinking=True)

        embed = message.embeds

        em = discord.Embed(color=config.cinza, description='')

        if not interaction.user.guild_permissions.kick_members:
            em.description = 'You do not have permissions for this'
            await interaction.edit_original_response(embed=em)
            return

        em.description = f'Inform a member \nex.: @biell'
        await interaction.edit_original_response(embed=em)

        def check(response: discord.Message):
            return response.author == interaction.user and response.channel == interaction.channel

        response: discord.Message = await self.bot.wait_for('message', check=check)

        try:
            membro = response.mentions[0]
        except:
            em.description = f'A member mention is needed'
            await interaction.edit_original_response(embed=em)
            return await response.delete()

        ind = -1
        for field in embed[0].fields:
            ind += 1
            if membro.mention in field.value:
                
                embed[0].set_field_at(ind, name=field.name, value=field.value.replace(f'\n{membro.mention}', ''))

                if not field.name.lower() == 'reserve':
                    embed[1].set_field_at(ind, name=embed[1].fields[ind].name, value=int(embed[1].fields[ind].value)+1)

                await message.edit(embeds=embed)

                em.description = f'**{membro.mention}** removed from **{field.name}**'
                await interaction.edit_original_response(embed=em)
                await response.delete()
                return

        em.description = f'**{membro.mention}** not found in this group'
        await interaction.edit_original_response(embed=em)
        await response.delete()
        return


async def setup(bot):
    await bot.add_cog(Raids_Context(bot))
