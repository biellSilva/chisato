import discord

from extensions import config


class GroupsView(discord.ui.View):

    @discord.ui.button(custom_id='0', label='Enter', style=discord.ButtonStyle.grey)
    async def button_enter(self, interaction: discord.Interaction, button: discord.ui.Button):

        '''Enter Button'''

        msg_edit = interaction.message
        embed = msg_edit.embeds
        user = interaction.user

        tof_member = interaction.guild.get_role(config.tof_member)

        em = discord.Embed(color=config.cinza, description='')

        if tof_member not in user.roles:
            em.description = f'Missing Role: {tof_member.mention}'
            em.title = 'Error'
            return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)

        for field in embed[0].fields:
            if user.mention in field.value:
                embed[0].set_field_at(0, name=field.name, value=field.value.replace(f'\n{user.mention}', ''))

                if len(embed[0].fields) == 2:
                    embed[0].set_field_at(1, name=embed[0].fields[1].name,value=int(embed[0].fields[1].value)+1)

                em.description = f'Removed from the group'
                await msg_edit.edit(embeds=embed)
                return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)

            embed[0].set_field_at(0, name=field.name, value=field.value+f'\n{user.mention}')

            if len(embed[0].fields) == 2:
                if int(embed[0].fields[int(button.custom_id)].value) <= 0:
                    em.description = f'This group is full'
                    await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)
                    return

                embed[0].set_field_at(1, name=embed[0].fields[1].name, value=int(embed[0].fields[1].value)-1)

            em.description = f'Added to the group'

            await msg_edit.edit(embeds=embed)
            return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)
            

    @discord.ui.button(custom_id='button_DEL', style=discord.ButtonStyle.grey, emoji='❌')
    async def button_DEL(self, interaction: discord.Interaction, button: discord.ui.Button):

        '''Delete'''

        em = discord.Embed(color=config.cinza, description='')

        if not interaction.user.guild_permissions.kick_members and interaction.user.id not in interaction.message.embeds[0].footer:
           em.description = 'You do not have permissions for this'
           return await interaction.response.send_message(embed=em, ephemeral=True, delete_after=10)

        await interaction.message.edit(view=None)
        await interaction.message.delete(delay=1)
