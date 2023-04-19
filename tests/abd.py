import requests
from bs4 import BeautifulSoup

tof_index = 'https://toweroffantasy.info'

# re = requests.get(url=f'{tof_index}/simulacra/fiona')
# simulacra_soup = BeautifulSoup(re.content, 'html.parser')

# attrs = simulacra_soup.find("div", class_="weapon-info svelte-knq7ru").find_next('div', class_='stats-wrapper svelte-knq7ru').find_next('div', class_='stats-wrapper svelte-knq7ru')

# for attr in attrs:
#     try:
#         print(attr.find('span').text.title(), attr.find('b').text.title())
#     except:
#         continue

# element = simulacra_soup.find('h5', class_='svelte-jf787x')
# element_text = element.find_next('p')

# print(element_text.text)

# estrelas = simulacra_soup.find('div', class_='table-wrapper advancements').find_next('tbody').find_all_next('tr', limit=6)

# value = ''
# for estrela in estrelas:
#     print(f'{estrela.find("th").text}: {estrela.find("p").text}\n\n')

# matrices = simulacra_soup.find('table', class_='bg-alternate').find_next('table', class_='bg-alternate').find_all_next('tr')

# for matrice in matrices:
#     print(matrice.find('i', class_='svelte-1991z96').text,
#           matrice.find('span', class_='svelte-1991z96').text, matrice.find('td').text)

# traits = simulacra_soup.find('div', class_='slider-wrapper awakening-traits svelte-ea8o5d').find_all_next('p')
# print('\n TRAIT 4000:')
# for trait in traits:
#     print(trait.text)

# traits = simulacra_soup.find('div', class_='slider-wrapper awakening-traits svelte-ea8o5d').find('p')
# print(traits)


re = requests.get(url=f'{tof_index}/matrices/marc')
matrice_soup = BeautifulSoup(re.content, 'html.parser')

print(matrice_soup.find('h1').text.upper() if matrice_soup.find('abbr') is None else matrice_soup.find('h1').text.upper() + ' [CN]')
print(f'{tof_index}/simulacra/fiona')
print(tof_index+'/'+matrice_soup.find('img', class_='bg-img svelte-mpn75').get('src'))

print('\n')

print(matrice_soup.find('h2', id='sets').text)
print(matrice_soup.find('div', class_='table-wrapper').find_next('tbody').text)