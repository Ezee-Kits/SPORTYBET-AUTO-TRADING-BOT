import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from func import match_day_date,main_date,saving_to_firebase,save_daily_csv,drop_duplicate




def forbet_func():
    print("Starting Playwright script...")
    full_path = save_daily_csv()
    path = path = f'{full_path}/forebet.csv'

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )

        context = browser.new_context(
            viewport={
                "width": random.randint(1280, 1920),
                "height": random.randint(720, 1080)
            },
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/122.0.0.0 Safari/537.36",
            locale="en-US",
            timezone_id="Africa/Lagos",
            java_script_enabled=True
        )

        page = context.new_page()

        _1x2url = f'https://www.forebet.com/en/football-predictions/predictions-1x2/{main_date()}'
        ovrund_url = f'https://www.forebet.com/en/football-predictions/under-over-25-goals/{main_date()}'
        btsots_url = f'https://www.forebet.com/en/football-predictions/both-to-score/{main_date()}'
        all_url = [_1x2url,ovrund_url,btsots_url]

        _1x2data = {
                'DATE':[],
                'TIME':[],

                'HOME TEAM': [],
                'AWAY TEAM': [],

                'HOME PER':[],
                'DRAW PER':[],
                'AWAY PER':[]}

        ovrund_data = {

                'HOME TEAM': [],
                'AWAY TEAM': [],

                'UNDER 2.5':[],
                'OVER 2.5':[]
                }
        btsund_data = {
                'HOME TEAM': [],
                'AWAY TEAM': [], 

                'BTS':[],
                'OTS':[],
                'NAME':[]
                }
        
        for main_url in all_url:
            print("Navigating to page...")
            page.goto(main_url, timeout=60000, wait_until="domcontentloaded")
            print("Page loaded successfully")

            for i in range(7):  # scroll 10 times
                page.evaluate('window.scrollBy(0, window.innerHeight)')
                time.sleep(1)

            for x in range(3):  # click MORE button 3 times
                try:
                    page.wait_for_selector('#mrows', state="visible", timeout=5000)
                    page.click('#mrows')
                    print(f'Clicked MORE button {x+1} times \n')
                except Exception as e:
                    print(f'Breaking Due To Error clicking MORE button: {e}')
                    break
                time.sleep(2)  # wait for 2 seconds after each click

            time.sleep(7)  # wait for 10 seconds after scrolling and clicking MORE buttons
            print('\n MORE CLICKED AND 10 SECONDS WAITED \n')

            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')
            all_content = soup.find('div', class_='schema')
            print('\n ALL CONTENT FETCHED \n')
            
            if main_url == _1x2url:
                print('\n CURRENTLY ON 1X2 OPTION \n')
                match_date = [(y.text.split())[0] for y in all_content.find_all('span', class_='date_bah')]
                match_time = [(y.text.split())[-1] for y in all_content.find_all('span', class_='date_bah')]
                hm_team = [y.text for y in all_content.find_all('span', class_='homeTeam')]
                aw_team = [y.text for y in all_content.find_all('span', class_='awayTeam')]
                # print(match_date, match_time, hm_team, aw_team) 

                hm_per = [y.find_all('span')[0].text for y in all_content.find_all('div', class_='fprc')]
                draw_per = [y.find_all('span')[1].text for y in all_content.find_all('div', class_='fprc')]
                aw_per = [y.find_all('span')[2].text for y in all_content.find_all('div', class_='fprc')]
                # print(hm_per, draw_per, aw_per)
                print(len(match_date), len(match_time), len(hm_team), len(aw_team), len(hm_per), len(draw_per), len(aw_per))
                _1x2data['DATE']= match_date
                _1x2data['TIME']= match_time
                _1x2data['HOME TEAM']= hm_team
                _1x2data['AWAY TEAM']= aw_team
                _1x2data['HOME PER']= hm_per
                _1x2data['DRAW PER']= draw_per
                _1x2data['AWAY PER']= aw_per


            elif main_url == ovrund_url:
                print('\n CURRENTLY ON OVER/UNDER OPTION \n')
                hm_team = [y.text for y in all_content.find_all('span', class_='homeTeam')]
                aw_team = [y.text for y in all_content.find_all('span', class_='awayTeam')]
                under_2_5 = [y.find_all('span')[0].text for y in all_content.find_all('div', class_='fprc')]
                over_2_5 = [y.find_all('span')[1].text for y in all_content.find_all('div', class_='fprc')]
                # print(hm_team,aw_team,under_2_5,over_2_5)
                print(len(hm_team), len(aw_team), len(under_2_5), len(over_2_5))
                ovrund_data['HOME TEAM']= hm_team
                ovrund_data['AWAY TEAM']= aw_team
                ovrund_data['UNDER 2.5']= under_2_5
                ovrund_data['OVER 2.5']= over_2_5

            else:
                print('\n CURRENTLY ON OTS/BTS OPTION \n')
                hm_team = [y.text for y in all_content.find_all('span', class_='homeTeam')]
                aw_team = [y.text for y in all_content.find_all('span', class_='awayTeam')]
                ots = [y.find_all('span')[0].text for y in all_content.find_all('div', class_='fprc')]
                bts = [y.find_all('span')[1].text for y in all_content.find_all('div', class_='fprc')]
                # print(hm_team,aw_team,bts,ots)
                print(len(hm_team), len(aw_team), len(bts), len(ots))
                btsund_data['HOME TEAM']= hm_team
                btsund_data['AWAY TEAM']= aw_team
                btsund_data['BTS']= bts
                btsund_data['OTS']= ots
                btsund_data['NAME']= 'Forebet'

        df1 = pd.DataFrame(_1x2data)
        df2 = pd.DataFrame(ovrund_data)
        df3 = pd.DataFrame(btsund_data)
        # print(df1.to_string())
        # print(df2.to_string())  
        # print(df3.to_string())
        print(len(df1), len(df2), len(df3))
        all_df = pd.merge(df1, df2, on=['HOME TEAM', 'AWAY TEAM'], how='inner')
        all_df = pd.merge(all_df, df3, on=['HOME TEAM', 'AWAY TEAM'], how='inner').reset_index(drop=True)
        all_df['1X PER'] = (((all_df['HOME PER'].astype(float)/100) + (all_df['DRAW PER'].astype(float)/100))*100).round()
        all_df['12 PER'] = (((all_df['HOME PER'].astype(float)/100) + (all_df['AWAY PER'].astype(float)/100))*100).round()
        all_df['X2 PER'] = (((all_df['AWAY PER'].astype(float)/100) + (all_df['DRAW PER'].astype(float)/100))*100).round()
        all_df['OVER 1.5'] = all_df['BTS'].astype(int) + 15
        
        print(all_df)

        all_df.to_csv(path, index=False)
        # saving_to_firebase(data=all_df,file_name='Forebet')
        print('============================= FIRST FILE SAVED ==========================')
        drop_duplicate(path=path)
        browser.close()

forbet_func()
