import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('season',
                    type = int,
                    help='Second half of season (2016-17 is entered as 2017)')

args = parser.parse_args()

x = pd.read_html('https://www.basketball-reference.com/leagues/NBA_' + str(args.season) + '_totals.html')
x = x[0]
x = x[pd.to_numeric(x['Rk'], errors='coerce').notnull()]