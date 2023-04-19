import discord
import requests

from discord import app_commands
from discord.ext import commands
from typing import Optional
from bs4 import BeautifulSoup

from extensions import config
from extensions.views.wiki_view import WikiView


class Info(commands.Cog):

    '''Info Commands'''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    info = app_commands.Group(name='info', description='Tower of Fantasy Index', guild_only=True)

    @info.command(name='simulacra')
    @app_commands.describe(name='Simulacra Name')
    @app_commands.checks.bot_has_permissions(send_messages=True)
    async def simulacra(self, interaction: discord.Interaction, name: Optional[str]):

        '''Simulacra info'''

        await interaction.response.defer()

        tof_index = 'https://toweroffantasy.info'

        em = discord.Embed(
            color=config.cinza, description='')

        if not name:
            re = requests.get(url=tof_index)
            soup = BeautifulSoup(re.content, 'html.parser')

            em.title = soup.find('a', class_='home-link svelte-170cp8q').text
            em.url = tof_index
            em.set_thumbnail(url=tof_index+'/'+soup.find('img', {'alt': 'Logo'}).get('src'))

            trs = soup.find_all('tr', class_='outer-tr svelte-9hfdzd')

            for tr in trs:
                value = ''
                tds = tr.find_all('td')

                value += f'Added to Standard: {tds[4].text} \n Newest: [{tds[3].text}]({tof_index}{tds[3].get("href")})\n\n'
                value += 'Current:\n'

                for banner in tds[0]:
                    value += f'[{banner.text}]({tof_index}{banner.get("href")})\n'
                
                em.add_field(name=tr.find('th').text, value=value)
            
            return await interaction.edit_original_response(embed=em)
        
        else:
            if 'tian' in name.lower():
                name = 'tian lang'
            if 'saki' in name.lower():
                name = 'saki fuwa'
            if 'cobalt' in name.lower():
                name = 'cobalt-b'
            if 'coco' in name.lower():
                name = 'coco ritter'
            if 'anna' in name.lower():
                name = 'annabella'
            if 'guno' in name.lower():
                name = 'gunonno'

            try:
                re = requests.get(url=f'{tof_index}/simulacra/{name.replace(" ", "-").lower()}')
                soup = BeautifulSoup(re.content, 'html.parser')

                em.title = soup.find('h1').text.upper() if soup.find('abbr') is None else soup.find('h1').text.upper() + ' [CN]'
                em.url = f'{tof_index}/simulacra/{name.replace(" ", "-")}'
                em.set_thumbnail(url=tof_index+'/'+soup.find('img', class_='bg-img svelte-mpn75').get('src'))
                em.set_footer(text='Home')

                em.description = f'**{soup.find("h3").text.title()}** | '

                for attr in soup.find_all('img', class_='svelte-ad2u0z'):
                    em.description += f'{attr.get("alt").title()} '

                em.description+='\n'

                for attr in soup.find("div", class_="weapon-info svelte-knq7ru").find_next('div', class_='stats-wrapper svelte-knq7ru').find_next('div', class_='stats-wrapper svelte-knq7ru'):
                    try:
                        em.description+=f' {attr.find("span").text.title()}: {attr.find("b").text.title()} \n'
                    except:
                        continue

                element = soup.find('h5', class_='svelte-jf787x')
                em.add_field(name=element.text.title(), value=element.find_next("p").text, inline=False)

                try:
                    element_res = element.find_next('h5', class_='svelte-jf787x')
                    em.add_field(name=element_res.text.title(), value=element_res.find_next("p").text, inline=False)
                except:
                    pass

                await interaction.edit_original_response(embed=em, view=WikiView(timeout=180))
            except AttributeError:
                em = discord.Embed(color=config.cinza, description=f'Couldn\'t find')
                return await interaction.edit_original_response(embed=em)


    @info.command(name='matrices')
    @app_commands.describe(name='Simulacra Name')
    @app_commands.checks.bot_has_permissions(send_messages=True)
    async def matrices(self, interaction: discord.Interaction, name: str):

        '''Matrices info'''

        await interaction.response.defer()

        tof_index = 'https://toweroffantasy.info'

        em = discord.Embed(color=config.cinza, description='')

        if 'tian' in name.lower():
            name = 'tian lang'
        if 'saki' in name.lower():
            name = 'saki fuwa'
        if 'cobalt' in name.lower():
            name = 'cobalt-b'
        if 'coco' in name.lower():
            name = 'coco ritter'
        if 'anna' in name.lower():
            name = 'annabella'
        if 'guno' in name.lower():
            name = 'gunonno'

        try:
            re = requests.get(url=f'{tof_index}/matrices/{name.replace(" ", "-").lower()}')
            soup = BeautifulSoup(re.content, 'html.parser')

            em.title = soup.find('h1').text.upper()+' Matrices' if soup.find('abbr') is None else soup.find('h1').text.upper() + ' Matrices [CN]'
            em.url = f'{tof_index}/matrices/{name.replace(" ", "-")}'
            em.set_thumbnail(url=tof_index+'/'+soup.find('img',class_='bg-img svelte-mpn75').get('src'))

            for txt in soup.find('div', class_='table-wrapper').find_next('tbody'):
                em.add_field(name='x'+txt.find('th').text, value=txt.find('p').text, inline=False)

            await interaction.edit_original_response(embed=em)
            return
        except AttributeError:
            em = discord.Embed(color=config.cinza, description=f'Couldn\'t find')
            return await interaction.edit_original_response(embed=em)


async def setup(bot):
    await bot.add_cog(Info(bot))
