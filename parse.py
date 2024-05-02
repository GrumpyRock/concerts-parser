import re
from bs4 import BeautifulSoup

with open("index.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')


concert_list = soup.css.select('[itemtype="https://schema.org/MusicEvent"]')

concerts = []

for raw_concert in concert_list:
    concert = {}
    concert['location_name'] = raw_concert.select('[itemprop="location"] [itemprop="name"]')[0]['content']
    concert['location_locality'] = raw_concert.select('[itemprop="location"] [itemprop="address"] [itemprop="addressLocality"]')[0]['content']
    concert['location_country'] = raw_concert.select('[itemprop="location"] [itemprop="address"] [itemprop="addressCountry"]')[0]['content']
    concert['name'] = raw_concert.select('[itemprop="name"]')[1]['content']
    concert['start_date'] = raw_concert.select('[itemprop="startDate"]')[0]['content']
    concert['end_date'] = raw_concert.select('[itemprop="endDate"]')[0]['content']

    concert['artists'] = []

    raw_html = raw_concert.select('td:last-child')[0]
    artists_html = raw_html.select('div.col')
    for sub_html in artists_html:
        concert['artists'].append({ 'name': sub_html.b.text, 'genres': re.split("/|,|\\|", sub_html.i.text) })

    concerts.append(concert)

print(concerts)