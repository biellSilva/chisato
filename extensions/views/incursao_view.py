import discord

from extensions import config


async def ensure_group(interaction: discord.Interaction, button: discord.ui.Button):
    msg_edit = interaction.message
    embed = msg_edit.embeds
    user = interaction.user

    tof_member = interaction.guild.get_role(config.tof_member)

    em = discord.Embed(color=config.cinza, description='')

    if tof_member not in user.roles:
        em.description=f'Missing Role: {tof_member.mention}'
        em.title='Error'
        return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)

    for field in embed[0].fields:
        if user.mention in field.value:
            if not button.label.lower() in field.name.lower():
                em.description = f'You already participate in **{field.name}**'
                return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)
            
            if button.label.lower() in field.name.lower():
                embed[0].set_field_at(int(button.custom_id), name=field.name, value=field.value.replace(f'\n{user.mention}', ''))

                if not button.label.lower() == 'reserve':
                    embed[1].set_field_at(int(button.custom_id), name=embed[1].fields[int(button.custom_id)].name,
                                      value=int(embed[1].fields[int(button.custom_id)].value)+1)

                em.description=f'Removed from **{field.name}**'
                
                await msg_edit.edit(embeds=embed)
                return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)

    for field in embed[0].fields:
        if button.label.lower() in field.name.lower():
            embed[0].set_field_at(int(button.custom_id), name=field.name, value=field.value+f'\n{user.mention}')

            if not button.label.lower() == 'reserve':

                if int(embed[1].fields[int(button.custom_id)].value) <= 0:
                    em.description=f'**{field.name}** is full'
                    await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)
                    return 
                
                embed[1].set_field_at(int(button.custom_id), name=embed[1].fields[int(button.custom_id)].name, 
                                      value=int(embed[1].fields[int(button.custom_id)].value)-1)

            em.description=f'Added to **{field.name}**'

            await msg_edit.edit(embeds=embed)
            return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)


class IncursaoView(discord.ui.View):

    @discord.ui.button(custom_id='0', label='DPS', style=discord.ButtonStyle.grey, emoji=config.dps)
    async def button_DPS(self, interaction: discord.Interaction, button: discord.ui.Button):

        '''DPS Button'''

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='1', label='SUP', style=discord.ButtonStyle.grey, emoji=config.sup)
    async def button_SUP(self, interaction: discord.Interaction, button: discord.ui.Button):

        '''Support Button'''

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='2', label='TANK', style=discord.ButtonStyle.grey, emoji=config.tank)
    async def button_TANK(self, interaction: discord.Interaction, button: discord.ui.Button):

        '''Tank Button'''

        await ensure_group(interaction, button)

    @discord.ui.button(custom_id='3', label='RESERVE', style=discord.ButtonStyle.grey)
    async def button_AUX(self, interaction: discord.Interaction, button: discord.ui.Button):

        '''Reserva Button'''

        await ensure_group(interaction, button)
        

    @discord.ui.button(custom_id='button_DEL', style=discord.ButtonStyle.grey, emoji='❌')
    async def button_DEL(self, interaction: discord.Interaction, button: discord.ui.Button):
       
        '''Delete'''

        em = discord.Embed(color=config.cinza, description='')

        if not interaction.user.guild_permissions.kick_members:
           em.description='You do not have permissions for this'
           return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)
       
        await interaction.message.edit(view=None)
        await interaction.message.delete(delay=1)



