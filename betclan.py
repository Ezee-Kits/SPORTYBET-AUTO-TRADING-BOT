
from func import requests_init,saving_files,saving_to_firebase,sorting_values,save_daily_csv,match_day_date,save_daily_csv2,main_date
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os




def betclan_func():
    full_path = save_daily_csv()
    path = path = f'{full_path}/betclan.csv'

    session = requests.Session()
    if match_day_date ==1:
        url = 'https://www.betclan.com/tomorrows-football-predictions/'
    else:
        url = 'https://www.betclan.com/todays-football-predictions/'



    soup,_ = requests_init(url)
    #   GETTING LINK SECTION
    links = [name.get('href') for name in soup.findAll('a')]
    # print(links)

    all_link = []
    for link in links:
        try:
            if link.startswith('https://www.betclan.com/predictionsdetails/') and link not in all_link:
                all_link.append(link)
        except:
            pass
    # USING LINKS TO GET ELEMENT IN THAT TEAMS
    print('LENGHT OF ALL LINKS = ',len(all_link))
    # all_link = all_link[170:]
    data = {
            'DATE':[],
            'TIME':[],
            
            'HOME TEAM': [],
            'AWAY TEAM': [],

            'HOME PER':[],
            'DRAW PER':[],
            'AWAY PER':[],
            '1X PER':[],
            '12 PER':[],
            'X2 PER':[],

            'OVER 1.5':[],
            'UNDER 2.5':[],
            'OVER 2.5':[],
            'BTS':[],
            'OTS':[],
            'NAME':[]
            }

    for i,x in enumerate(all_link[:]):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
        print('\n url = ',x)

        
        index_pos = i
        print(f'>>>>>>>>>>>>>>>>>>>>  NUMBER = {index_pos} HAS STARTED TO RUN, WITH TOTAL RUNS OF {len(all_link)}  & REMANING OF {len(all_link) - (index_pos+1)} <<<<<<<<<<<<<<<<<<<< \n')
        
        try:
            res = session.get(x, headers=headers, timeout=(5, 10))
            soup = BeautifulSoup(res.content,"html.parser")

            preds = [x.text.strip().replace('%','').split() for x in soup.find_all('div',class_ = 'cell vote__stats js-vote-stats-container')]
            # _,tree = requests_init(url=x)
            date_time = soup.find('span',class_ = 'dategamedetailsis').text.strip().split()
            teams = soup.find('div',class_ = 'teamstop').text.strip().split('\n')
            home_team = teams[0]
            away_team = teams[-1]
            
            hw = int(preds[0][1])
            draw = int(preds[0][3])
            aw = int(preds[0][5])

            under = int(preds[1][1])
            over = int(preds[1][3])

            bts = int(preds[2][1])
            ots = int(preds[2][3])

            print(date_time,home_team,away_team,hw,draw,aw,under,over,bts,ots)

            data['DATE'].append(date_time[1])
            data['TIME'].append(date_time[2])

            data['HOME TEAM'].append(home_team)
            data['AWAY TEAM'].append(away_team)

            data['HOME PER'].append(hw)
            data['DRAW PER'].append(draw)
            data['AWAY PER'].append(aw)

            data['1X PER'].append( round(((hw/100) + (draw/100))*100) )
            data['12 PER'].append( round(((hw/100) + (aw/100))*100) )
            data['X2 PER'].append( round(((aw/100) + (draw/100))*100) )

            data['UNDER 2.5'].append(under)
            data['OVER 2.5'].append(over)

            data['OVER 1.5'].append(bts+15)
            data['BTS'].append(bts)
            data['OTS'].append(ots)
            data['NAME'].append('BCL')
        except:
            print('\n \n SORRY AN ERROR OCCURED \n')
            pass

    # saving_to_firebase(data=data,file_name='Betclan')
    saving_files(data=data,path=path)

betclan_func()
