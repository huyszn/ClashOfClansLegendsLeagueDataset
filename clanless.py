import requests
import pandas as pd

token = ""
headers = {'authorization': 'Bearer ' +token,'Accept': 'application/json' }

tag = ""

# Manually input a player tag
# while True:
#     tag = input("Enter the player tag: ")
#     tag = tag.replace("#","")
#     response_json = requests.get('https://api.clashofclans.com/v1/players/%23'+ tag, headers=headers).json()
#     try:
#         print(response_json['clan']['name'])
#     except KeyError:
#         print("Not in a clan")
#         print(response_json['name'])
#         print(response_json['warStars'], 'war stars')
#         if response_json['townHallLevel'] >= 13:
#             print('Town hall', response_json['townHallLevel'])
#         else:
#             print('Low level Town hall', response_json['townHallLevel'])
#         if response_json['clanCapitalContributions'] == 0:
#             print('0 clan capital contributions')
#         elif response_json['clanCapitalContributions'] < 100000:
#             print('Bad clan capital contributions:', response_json['clanCapitalContributions'])
#         else:
#             print('Clan capital contributions:', response_json['clanCapitalContributions'])

# Get random sample of n clanless players
file = '2022-10.csv'
n = 100
df = pd.read_csv(file)
df_random = df.sample(n=n)
for i in range(len(df_random)):
    tag = df_random.iloc[i]['tag']
    tag = tag.replace("#","")
    response_json = requests.get('https://api.clashofclans.com/v1/players/%23'+ tag, headers=headers).json()
    try:
        clan = response_json['clan']['name']
    except KeyError:
        #print('\n' * 5)
        try:
            name = response_json['name']
            #print("Not in a clan")
            print(name)
            print('#'+tag)
            print(response_json['warStars'], 'war stars')
            if response_json['townHallLevel'] >= 13:
                print('Town hall', response_json['townHallLevel'])
            else:
                print('Low level Town hall', response_json['townHallLevel'])
            if response_json['clanCapitalContributions'] == 0:
                print('0 clan capital contributions')
            elif response_json['clanCapitalContributions'] < 100000:
                print('Bad clan capital contributions:', response_json['clanCapitalContributions'])
            else:
                print('Clan capital contributions:', response_json['clanCapitalContributions'])
            print('\n')
        except KeyError:
            #print('Banned/Unknown')
            pass