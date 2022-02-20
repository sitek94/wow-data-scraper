import urllib.request
import re
from bs4 import BeautifulSoup

base_url = 'https://www.wowdb.com/achievements'

html = urllib.request.urlopen(base_url).read()
soup = BeautifulSoup(html, features="html.parser")

items = []

# Table structure, has the following structure, so it's "very convenient" to
# search for the data we want 🙈
#   <tr>
#     <td class="col-name">   - Name
#     <td>                    - Description
#     <td class="col-c">      - Fraction
#     <td>                    - Points
#     <td class="col-c>       - Category
#   </tr>

rows = soup.select('table#achievements > tbody > tr')
for row in rows:
    # GET ALL NEEDED CELLS

    # Name cell, get: name, description and icon url
    [name_td] = row.select('td.col-name')

    # Fraction cell, get fraction: "horde", "alliance" or nothing
    [fraction_td] = row.select('td.col-name + td')

    # Points cell, first cell with "col-c" is the one with the points
    points_td = row.select('td.col-name ~ td.col-c')[0]

    # ⏩ Omit reward cell
    # reward_td

    # Category cell, it's the last one
    [category_td] = row.select('td.col-name ~ td:last-child')

    # EXTRACT DATA FROM CELLS
    name = name_td.select('a.t')[0].text
    description = name_td.select('.subtext')[0].text
    icon_url = name_td.select('.listing-icon img')[0]['src']

    fraction = None
    fraction_content = fraction_td.select('span')
    if len(fraction_content) > 0:
        fraction = fraction_content[0].text
        if re.search('horde', fraction, re.IGNORECASE):
            fraction = 'horde'
        else:
            fraction = 'alliance'

    points = None
    points_content = points_td.select('span')
    if points_content:
        points = int(points_content[0].text.strip())

    category = category_td.text

    print(f'{name} - {description} - {fraction} - {points} - {category_td.text}')
