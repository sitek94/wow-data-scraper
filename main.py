import urllib.request

from bs4 import BeautifulSoup

base_url = 'https://www.wowdb.com/achievements'
download_dir = 'downloads'

html = urllib.request.urlopen(base_url).read()
soup = BeautifulSoup(html, features="html.parser")

items = []

rows = soup.select('table#achievements > tbody > tr')
for row in rows:
    print('hello 2')
