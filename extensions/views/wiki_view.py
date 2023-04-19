import discord
import requests

from bs4 import BeautifulSoup

from extensions import config


class WikiView(discord.ui.View):

    @discord.ui.button(custom_id='main', label='Home', style=discord.ButtonStyle.grey)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        '''Home Button'''
        await home(interaction, button)

    @discord.ui.button(custom_id='advancements', label='Advancements', style=discord.ButtonStyle.grey)
    async def advance_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        '''advancements Button'''
        await advance(interaction, button)

    @discord.ui.button(custom_id='matrices', label='Matrices', style=discord.ButtonStyle.grey)
    async def matrices_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        '''matrices Button'''
        await matrices(interaction, button)

    @discord.ui.button(custom_id='trait', label='Awakening', style=discord.ButtonStyle.grey)
    async def trait_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        '''trait Button'''
        await trait(interaction, button)


async def home(interaction: discord.Interaction, button: discord.ui.Button):

    await interaction.response.defer()

    '''Home Edit'''

    msg_edit = interaction.message
    em = msg_edit.embeds

    re = requests.get(url=em[0].url)
    soup = BeautifulSoup(re.content, 'html.parser')

    em[0].set_footer(text='Home')
    em[0].clear_fields()

    element = soup.find('h5', class_='svelte-jf787x')
    em[0].add_field(name=element.text.title(), value=element.find_next("p").text, inline=False)

    try:
        element_res = element.find_next('h5', class_='svelte-jf787x')
        em[0].add_field(name=element_res.text.title(), value=element_res.find_next("p").text, inline=False)
    except:
        pass

    await interaction.message.edit(embeds=em)
    return


async def advance(interaction: discord.Interaction, button: discord.ui.Button):

    await interaction.response.defer()

    '''Advancements Edit'''

    msg_edit = interaction.message
    embed = msg_edit.embeds

    re = requests.get(url=embed[0].url)
    soup = BeautifulSoup(re.content, 'html.parser')

    embed[0].set_footer(text='Advancements')
    embed[0].clear_fields()

    estrelas = soup.find('div', class_='table-wrapper advancements').find_next('tbody').find_all_next('tr', limit=6)

    for estrela in estrelas:
        embed[0].add_field(name=estrela.find("th").text, value=estrela.find("p").text, inline=False)

    await msg_edit.edit(embeds=embed)
    return


async def matrices(interaction: discord.Interaction, button: discord.ui.Button):

    await interaction.response.defer()

    '''Matrices Edit'''

    msg_edit = interaction.message
    embed = msg_edit.embeds

    re = requests.get(url=embed[0].url)
    soup = BeautifulSoup(re.content, 'html.parser')

    embed[0].set_footer(text='Recommended Matrices')
    embed[0].clear_fields()

    matrices = soup.find('table', class_='bg-alternate').find_next('table', class_='bg-alternate').find_all_next('tr')

    for matrice in matrices:
        embed[0].add_field(
            name=f"{matrice.find('i', class_='svelte-1991z96').text} {matrice.find('span', class_='svelte-1991z96').text}", value=matrice.find('td').text, inline=False)
    
    await interaction.message.edit(embeds=embed)
    return


async def trait(interaction: discord.Interaction, button: discord.ui.Button):

    await interaction.response.defer()

    '''Trait Edit'''

    msg_edit = interaction.message
    embed = msg_edit.embeds

    re = requests.get(url=embed[0].url)
    soup = BeautifulSoup(re.content, 'html.parser')

    embed[0].set_footer(text='Awakening - Traits')
    embed[0].clear_fields()

    traits = soup.find('div', class_='slider-wrapper awakening-traits svelte-ea8o5d').find_all_next('p')
    txt = ''
    for trait in traits:
        txt+=f'{trait.text}\n'

    embed[0].add_field(name='Affinity 4000', value=txt, inline=False)
    await interaction.message.edit(embeds=embed)
    return
