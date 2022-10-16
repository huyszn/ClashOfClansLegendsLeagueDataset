import requests
import argparse
import sys
from datetime import date
import pandas as pd

# Get API token from https://developer.clashofclans.com/#/account
token = ""

headers = {'authorization': 'Bearer ' +(token),'Accept': 'application/json' }

# Parse arguments
parser = argparse.ArgumentParser(description='Scrapes legends league data from the Clash of Clans API')
parser.add_argument('--season', '-s', action='store_true', help='Scrape one specific legends league season', required=False)
parser.add_argument('--latest', '-l', action='store_true', help='Scrape latest completed legends league season', required=False)
args = parser.parse_args()

def scrape_all_legends_league():
    # First Legend League Season: 2015-07
    year = 2015
    month = 7
    while True:
        season = str(year)+'-'+ '{0:02d}'.format(month)
        print(f'Downloading legends league data for the {season} season.')
        response = requests.get('https://api.clashofclans.com/v1/leagues/29000022/seasons/'+season, headers=headers)
        season_json = response.json()['items']
        season_df = pd.json_normalize(season_json)
        # rank to the first column
        rank = season_df.pop('rank')
        season_df.insert(0, rank.name, rank)
        # fill missing ranks with empty rows
        season_df = season_df.set_index('rank').reindex(range(1,season_df['rank'].iloc[-1])).fillna(0).reset_index()
        # change to int
        season_df['expLevel'] = season_df['expLevel'].astype(int)
        season_df['trophies'] = season_df['trophies'].astype(int)
        season_df['attackWins'] = season_df['attackWins'].astype(int)
        season_df['defenseWins'] = season_df['defenseWins'].astype(int)
        season_df.to_csv(f'data/{season}.csv', index=False)
        month += 1
        if month > 12:
            month = 1
            year += 1
        print('Download complete.')
        #Exit when month and year reach current season
        if month > date.today().month - 1 and year > date.today().year - 1:
            sys.exit(1)

def scrape_legends_league_season():
    # Manually input month and year
    while True:
        year = input('Enter the year you wish to get legends league season data: ')

        if year and int(year) >= 2015 and int(year) <= date.today().year:
            break
        print('Invalid year entered.')
    while True:
        month = input('Enter the month you wish to get legends league season data: ')

        if month and int(month) >= 1 and int(month) <= 12:
            break
        print('Invalid month entered.')
    try:
        season = year+'-'+ '{0:02d}'.format(int(month))
        print(f'Downloading legends league data for the {season} season.')
        response = requests.get('https://api.clashofclans.com/v1/leagues/29000022/seasons/'+season, headers=headers)
        season_json = response.json()['items']
        season_df = pd.json_normalize(season_json)
        # rank to the first column
        rank = season_df.pop('rank')
        season_df.insert(0, rank.name, rank)
        # fill missing ranks with empty rows
        season_df = season_df.set_index('rank').reindex(range(1,season_df['rank'].iloc[-1])).fillna(0).reset_index()
        # change to int
        season_df['expLevel'] = season_df['expLevel'].astype(int)
        season_df['trophies'] = season_df['trophies'].astype(int)
        season_df['attackWins'] = season_df['attackWins'].astype(int)
        season_df['defenseWins'] = season_df['defenseWins'].astype(int)
        season_df.to_csv(f'data/{season}.csv', index=False)
        print('Download complete.')
    except KeyError:
        print(f'Season {season} has not begun yet or has not ended yet.')


def scrape_latest_legends_league_season():
    # latest completed season's month and year
    year = date.today().year
    month = date.today().month - 1
    # if it is january, the get december season of last year
    if date.today().month == 1:
        year = date.today().year - 1
        month = 12
    season = str(year)+'-'+ '{0:02d}'.format(month)
    print(f'Downloading legends league data for the {season} season.')
    response = requests.get('https://api.clashofclans.com/v1/leagues/29000022/seasons/'+season, headers=headers)
    season_json = response.json()['items']
    season_df = pd.json_normalize(season_json)
    # rank to the first column
    rank = season_df.pop('rank')
    season_df.insert(0, rank.name, rank)
    # fill missing ranks with empty rows
    season_df = season_df.set_index('rank').reindex(range(1,season_df['rank'].iloc[-1])).fillna(0).reset_index()
    # change to int
    season_df['expLevel'] = season_df['expLevel'].astype(int)
    season_df['trophies'] = season_df['trophies'].astype(int)
    season_df['attackWins'] = season_df['attackWins'].astype(int)
    season_df['defenseWins'] = season_df['defenseWins'].astype(int)
    season_df.to_csv(f'data/{season}.csv', index=False)
    print('Download complete.')

if __name__ == '__main__':
    if args.season:
        scrape_legends_league_season()
    elif args.latest:
        scrape_latest_legends_league_season()
    else:
        scrape_all_legends_league()