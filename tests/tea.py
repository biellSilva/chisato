import requests
from bs4 import BeautifulSoup


re = requests.get(url='https://toweroffantasy.info')
soup = BeautifulSoup(re.content, features='lxml')

# trs = soup.find_all('tr', class_='outer-tr svelte-9hfdzd')
# for tr in trs:
#     print(tr.find('th').text)
#     banners = tr.find('td')

# for banner in banners:
#     print(banner.get("style").split("-")[-1].replace(")", "").title())

trs = soup.find_all('tr', class_='outer-tr svelte-9hfdzd')

assets = soup.find_all(
    'tbody', class_='banner-table collapse svelte-97quhy')

ind = 0
for tr in trs:
    value = ''
    tds = tr.find_all('td')

    for banner in tds[0]:
        ind = 0

        div_assets = assets.find_all('img')
        print(div_assets)

    #     value += f'[{banner.text}] - {banner.get("style").split("-")[-1].replace(")", "").title()}\n'

    # ind += 1
