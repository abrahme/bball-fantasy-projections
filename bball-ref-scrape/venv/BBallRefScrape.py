import pandas as pd
import argparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('start_season',
                    type = int,
                    help='Second half of season (2016-17 is entered as 2017)')
parser.add_argument('end_season',
                    type = int,
                    help='Second half of season (2016-17 is entered as 2017)')

args = parser.parse_args()

seasons = list(range(args.start_season, args.end_season + 1))

print(seasons)

full_df = pd.DataFrame()

for season in seasons:

    url = 'https://www.basketball-reference.com/leagues/NBA_' + str(season) + '_totals.html'
    x = pd.read_html(url)
    x = x[0]
    x = x[pd.to_numeric(x['Rk'], errors='coerce').notnull()]



    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    links = []
    for tr in table.findAll("tr"):
        trs = tr.findAll("td")
        for each in trs:
            try:
                link = each.find('a')['href']
                links.append(link)
            except:
                pass

    links = [y for y in links if not y.startswith('/teams')]
    x['ID'] = links
    x['ID'] = x['ID'].str[11:]
    x['ID'] = x['ID'].str.rstrip('.html')
    x['Season'] = season
    print(full_df.head())
    print(x.head())
    print(season)
    full_df = pd.concat([full_df, x])

print(full_df.head())
print(full_df.columns)
print(full_df.iloc[1004:1010,:])

filename = str(args.start_season) + '-' + str(args.end_season) + '_box_score_data.csv'

full_df.to_csv(filename, index = False)