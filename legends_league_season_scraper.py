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

def scrape_legends_league_season(year, month):
    season = f"{year}-{month:02d}"
    base_url = f'https://api.clashofclans.com/v1/leagues/29000022/seasons/{season}?limit=25000'
    season_df = pd.DataFrame()  # Create an empty dataframe to hold the data
    cursor = None
    print(f'Downloading legends league data for the {season} season.')
    
    try:
        while True:
            # Construct the URL with cursor (if applicable)
            url = base_url + (f'&after={cursor}' if cursor else '')
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            season_json = data['items']
            temp_df = pd.json_normalize(season_json)
            
            # Append the new data to the existing dataframe
            season_df = pd.concat([season_df, temp_df], ignore_index=True)
            
            # Check if there's another page
            if 'cursors' in data.get('paging', {}):
                cursor = data['paging']['cursors'].get('after')
                if not cursor:
                    break  # No more pages
            else:
                break  # No more pages
        
        # Process the final dataframe
        rank = season_df.pop('rank')
        season_df.insert(0, rank.name, rank)
        # fill missing ranks with empty rows
        season_df = season_df.set_index('rank').reindex(range(1, season_df['rank'].iloc[-1])).fillna(0).reset_index()
        # change to int
        season_df['expLevel'] = season_df['expLevel'].astype(int)
        season_df['trophies'] = season_df['trophies'].astype(int)
        season_df['attackWins'] = season_df['attackWins'].astype(int)
        season_df['defenseWins'] = season_df['defenseWins'].astype(int)
        
        # Save the final dataframe to a CSV file
        season_df.to_csv(f'data/{season}.csv', index=False)
        print(f'Download complete for {season} season.')
    
    except requests.exceptions.RequestException as e:
        # Handle any request errors and save the dataframe to CSV
        print(f'Error encountered: {e}. Saving the downloaded data...')
        season_df.to_csv(f'data/{season}_partial.csv', index=False)
        print(f'Partial data saved to data/{season}_partial.csv')
    except KeyError:
        print(f'Season {season} has not begun yet or has not ended yet.')

def scrape_all_legends_league():
    # First Legend League Season: 2015-07
    year = 2015
    month = 7
    while True:
        scrape_legends_league_season(year, month)
        
        # Increment the month and year
        month += 1
        if month > 12:
            month = 1
            year += 1

        # Exit when reaching the current season
        if year == date.today().year and month == date.today().month - 1:
            print("All seasons downloaded up to the latest available season.")
            sys.exit(1)


def scrape_latest_legends_league_season():
    # Get the latest completed season's month and year
    year = date.today().year
    month = date.today().month - 1
    
    # If it's January, get the December season of the previous year
    if date.today().month == 1:
        year = date.today().year - 1
        month = 12

    scrape_legends_league_season(year, month)

def prompt_user_for_season():
    # Prompt user for year and month
    while True:
        try:
            year = int(input('Enter the year (>= 2015) you wish to get legends league season data: '))
            if 2015 <= year <= date.today().year:  # Prevent entering future years
                break
            else:
                print(f"Please enter a valid year between 2015 and {date.today().year}.")
        except ValueError:
            print("Invalid input. Please enter a numeric year.")
    
    while True:
        try:
            month = int(input('Enter the month (1-12) you wish to get legends league season data: '))
            if 1 <= month <= 12:
                if year == date.today().year and month >= date.today().month:
                    print(f"Cannot download future data for {year}-{month}.")
                else:
                    break
            else:
                print("Please enter a valid month (1-12).")
        except ValueError:
            print("Invalid input. Please enter a numeric month.")

    scrape_legends_league_season(year, month)

if __name__ == '__main__':
    if args.season:
        prompt_user_for_season()
    elif args.latest:
        scrape_latest_legends_league_season()
    else:
        scrape_all_legends_league()