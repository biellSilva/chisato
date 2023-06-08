import discord

from extensions import config


async def ensure_group(interaction: discord.Interaction, button: discord.ui.Button):

    await interaction.response.defer(ephemeral=True, thinking=True)

    tof_member = interaction.guild.get_role(config.tof_member)

    em = discord.Embed(color=config.cinza, description='')

    if tof_member not in interaction.user.roles:
        em.description = f'Missing Role: {tof_member.mention}'
        em.title = 'Error'
        return await interaction.edit_original_response(embed=em)

    for color_id in config.colors_list:
        color = interaction.guild.get_role(color_id)
        if color in interaction.user.roles:
            await interaction.user.remove_roles(color)
            em.description+=f'Removed {color.mention}\n'
    
    color_add = interaction.guild.get_role(config.colors_list[int(button.custom_id)-1])
    await interaction.user.add_roles(color_add)

    em.description += f'\nAdded {color_add.mention}\n'

    await interaction.edit_original_response(embed=em)
    return


class ColorsView(discord.ui.View):

    @discord.ui.button(custom_id='1', label='01', style=discord.ButtonStyle.grey)
    async def button_1(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='2', label='02', style=discord.ButtonStyle.grey)
    async def button_2(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='3', label='03', style=discord.ButtonStyle.grey)
    async def button_3(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='4', label='04', style=discord.ButtonStyle.grey)
    async def button_4(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='5', label='05', style=discord.ButtonStyle.grey)
    async def button_5(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='6', label='06', style=discord.ButtonStyle.grey)
    async def button_6(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='7', label='07', style=discord.ButtonStyle.grey)
    async def button_7(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='8', label='08', style=discord.ButtonStyle.grey)
    async def button_8(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='9', label='09', style=discord.ButtonStyle.grey)
    async def button_9(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)
    
    @discord.ui.button(custom_id='10', label='10', style=discord.ButtonStyle.grey)
    async def button_10(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='11', label='11', style=discord.ButtonStyle.grey)
    async def button_11(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='12', label='12', style=discord.ButtonStyle.grey)
    async def button_12(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)
    
    @discord.ui.button(custom_id='13', label='13', style=discord.ButtonStyle.grey)
    async def button_13(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='14', label='14', style=discord.ButtonStyle.grey)
    async def button_14(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='15', label='15', style=discord.ButtonStyle.grey)
    async def button_15(self, interaction: discord.Interaction, button: discord.ui.Button):

        await ensure_group(interaction, button)
