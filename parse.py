import re
import json
from bs4 import BeautifulSoup

with open("index.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')


concert_list = soup.css.select('[itemtype="https://schema.org/MusicEvent"]')

concerts = []

for id_concert, raw_concert in enumerate(concert_list):
    concert = {}
    concert['id'] = id_concert
    concert['location_name'] = raw_concert.select('[itemprop="location"] [itemprop="name"]')[0]['content'].replace("\\\\", "\\")
    concert['location_locality'] = raw_concert.select('[itemprop="location"] [itemprop="address"] [itemprop="addressLocality"]')[0]['content']
    concert['location_country'] = raw_concert.select('[itemprop="location"] [itemprop="address"] [itemprop="addressCountry"]')[0]['content']
    concert['name'] = raw_concert.select('[itemprop="name"]')[1]['content']
    concert['start'] = raw_concert.select('[itemprop="startDate"]')[0]['content']
    concert['end'] = raw_concert.select('[itemprop="endDate"]')[0]['content']

    concert['artists'] = []

    last_child = raw_concert.select('td:last-child')

    concerts.append(concert)

html_concert_list = soup.css.select('tbody tr td:last-child')

# A faire : vérifier que les éléments des deux listes correspondent
for index, raw_html_concert in enumerate(html_concert_list):
    artists_html = raw_html_concert.select('div.col')
    concerts[index]['title'] = ""
    for sub_html in artists_html:
        concerts[index]['artists'].append({ 'name': sub_html.b.text, 'genres': re.split("/|,|\\|", sub_html.i.text) })
        concerts[index]['title'] += " + " if concerts[index]['title'] else " "
        concerts[index]['title'] += sub_html.b.text

print(json.dumps(concerts, ensure_ascii=False))