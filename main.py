import csv
import os.path
import re

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.wowdb.com/achievements'


def scrape_single_page(page_html):
    achievements = []
    soup = BeautifulSoup(page_html, features="html.parser")

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

        achievements.append([name, description, category, fraction, points, icon_url])
    return achievements


def scrape_achievements(first_page=1, last_page=2):
    all_achievements = []

    with requests.Session() as request:
        for i in range(first_page, last_page + 1):
            page_url = base_url + '?page=' + str(i)

            html = request.get(page_url).text
            achievements = scrape_single_page(html)
            all_achievements.extend(achievements)
            print(f'Page {i}: Scraped {len(achievements)} achievements...')

    print(f'Scraped {len(all_achievements)} achievements in total!')
    return all_achievements


scraped = scrape_achievements(1, 4)


def write_to_file(achievements):
    if not os.path.exists('data'):
        os.mkdir('data')

    with open('data/achievements.csv', 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)

        header = ['name', 'description', 'category', 'fraction', 'points', 'icon_url']
        writer.writerow(header)

        for achievement in achievements:
            writer.writerow(achievement)


write_to_file(scraped)
