
from func import firebase_read_and_save,place_bet,sort_by_name_and_time_exact,click_center,main_date,save_daily_csv2
from playwright.sync_api import sync_playwright
from datetime import datetime
from Login import Login_to
from Main_Calc import cal
import pandas as pd
import warnings
import random
import time
import os
warnings.simplefilter(action='ignore',category=pd.errors.PerformanceWarning)



other_days_values = datetime.today().weekday()

percent = 55 # DATA SORTING PERCENT
Err_Timeout = 3000 # WEBPAGE TIMEOUT 


# default values (normal days)
A_edge = 0.05 # ACCEPTED EDGE
FA3W_percent = 55 # FORBET ACCEPTED 3WAY PERCENT
FA_OVRUND_percent = 60 # FORBET ACCEPTED OVER/UNDER PERCENT
FA_BTTS_percent = 60 # FORBET ACCEPTED BOTH TEAMS TO SCORE PERCENT
other_check = 52
agree_no = 2


weights = {
    'ACC': 0.8,  # Accumulator Generator
    'BCL': 1.0,  # Betclan
    'FST': 0.9,  # FootballSuperTips
    'FRB': 1.4,  # Forebet
    'PRE': 1.1,  # Prematips
    'STA': 1.2   # Statarea
}

csv_files_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'CSV FILES/{str(main_date())} Files')
save_dir = save_daily_csv2(main_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES'),second_dir_path_name=str(main_date())+' Main_Files')
save_path = f'{save_dir}/Data.csv'

# # Read the CSV files
acc_df_f = pd.read_csv(f'{csv_files_path}/accumulator.csv')
bcl_df_f = pd.read_csv(f'{csv_files_path}/betclan.csv')
fst_df_f = pd.read_csv(f'{csv_files_path}/footballsupertips.csv')
frb_df_f = pd.read_csv(f'{csv_files_path}/forebet.csv')
pre_df_f = pd.read_csv(f'{csv_files_path}/prematips.csv')
sta_df_f = pd.read_csv(f'{csv_files_path}/statarea.csv')


print("All DataFrames ready! Continuing script...")


def SportyBet_func():
    global acc_df, bcl_df, fst_df, frb_df, pre_df, sta_df,weights
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
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
    
        url = 'https://www.sportybet.com/ng/sport/football/today'
        print('PLAYWRIGHT LOADED SUCCESFULLY AND WAITING TO EXECUTE THE URL')
        page.goto(url=url,timeout = 50000,wait_until="networkidle")
        Login_to(page)

        running = True
        next_page = 2
        while running:
            for fir_match in range(2,100): # MAIN LAYER (2 MINIMUM VALUE)
                print(f'\n [[CURRENTLY ON PAGINATION PAGE]] : {next_page-1} & FIRST-MATCH BOX NUMBER {fir_match}\n')
                try:
                    page.wait_for_selector(f'xpath=//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]', timeout=Err_Timeout)
                    xpath = f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]'
                    page.locator(f"xpath={xpath}").first.scroll_into_view_if_needed()
                    print(f'CONTENT CONTAINER FOUND ON FIRST MATCH NUMBER : {fir_match}')
                except:
                    try:
                        for avaliable_next_match in range(1,6):
                            print(f'TRYING OTHER CONTAINER FIRST MATCH, IF AVALIABLE :{avaliable_next_match}:')
                            fir_match +=avaliable_next_match
                            try:
                                page.wait_for_selector(f'xpath=//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]', timeout=1000)
                                xpath_first = f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]'
                                page.locator(f"xpath={xpath_first}").first.scroll_into_view_if_needed()
                                print(f'OTHER CONTENT CONTAINER FOUND ON :{avaliable_next_match}:')
                                break
                            except:
                                print(f'OTHER CONTENT CONTAINER NOT FOUND YET ON :[{avaliable_next_match}]:')
                            if avaliable_next_match == 5:
                                raise ValueError('No more matches found on this page.')
                    except:
                        is_disabled =  page.locator('span.icon-next.icon-disabled')
                        is_NextAvaliable = page.locator('.pagination.pagination span.icon-next:not(.icon-disabled)')
                        
                        if is_disabled.count() > 0:
                            print("\n✅ Reached the last page. No more next pages to click.\n")
                            running = False
                            break                        
                        elif is_NextAvaliable.count() > 0:
                            print("\n➡️ Clicking on Next page...\n")
                            click_center(page, '//div[@class="pagination pagination"]/span[contains(@class,"icon-next")]')
                            page.wait_for_selector('xpath=//*[@id="importMatch"]/div[2]/div/div[3]/div[1]', timeout=20000)
                            print(f'\n CLICKED ON NEXXT PAGE : {next_page}\n')
                            next_page +=1
                            break
                        else:
                            print("\n✅ No more new next pages to click exist.✅ \n")
                            running = False
                            break

                pp_data = {'INFO':[]}
                for sec_match in range(2,100): # SUB LAYER (2 MINIMUM VALUE)
                    print(f'\n CURRENTLY ON SPORTY NUMBER >>>> {fir_match} ON {sec_match}\n')
                    # Wait for the element to appear
                    try:
                        selector = f'xpath=//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]'
                        element = page.wait_for_selector(selector, timeout=Err_Timeout)
                        element.text_content()   # equivalent to getProperty('textContent')
                    except:
                        break

                    # Scroll element into view
                    try:
                        element.evaluate("""
                            el => el.scrollIntoView({
                                behavior: "smooth",
                                block: "center"
                            })
                        """)
                    except:
                        print('error on 1 scroll')
                        break
                    # Scroll again to ensure visibility
                    try:
                        element.evaluate("""
                            el => el.scrollIntoView({
                                behavior: "smooth",
                                block: "center"
                            })
                        """)
                    except:
                        print('error on 2 scroll')
                        break
                    # Extract text values

                    print('currently on data extraction')
                    try:
                        date_elem = page.wait_for_selector(
                            f'xpath=//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[1]/div[1]',
                            timeout=Err_Timeout
                        )
                        spt_date = date_elem.text_content().split()[0]
                        spt_date = datetime.strptime(f"2025/{spt_date}", "%Y/%d/%m").strftime("%Y-%m-%d")

                        time_elem = page.wait_for_selector(
                            f'xpath=//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[1]/div[1]',
                            timeout=Err_Timeout
                        )
                        spt_time = time_elem.text_content().strip()

                        home_elem = page.wait_for_selector(
                            f'xpath=//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[1]',
                            timeout=Err_Timeout
                        )
                        spt_home_team = home_elem.text_content().strip().replace('SRL','SIMULATED REALITY LEAGUE')
                        away_elem = page.wait_for_selector(
                            f'xpath=//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[2]',
                            timeout=Err_Timeout)
                        spt_away_team = away_elem.text_content().strip().replace('SRL','SIMULATED REALITY LEAGUE')

                    except:
                        print('error on data extraction section')
                        break
                    print(spt_date, spt_time, spt_home_team, spt_away_team)

                    pp_target = f'{spt_date}-{spt_time}-{spt_home_team}-{spt_away_team}'
                    pp_data['INFO'].append(pp_target)             
                    try:
                        pp_data_df = pd.read_csv(save_path)['INFO'].to_list()
                    except:
                        pp_data_df = pd.DataFrame({'INFO':['starting']})['INFO'].to_list()

                    if pp_target not in pp_data_df:
                        acc_df = sort_by_name_and_time_exact(acc_df_f, spt_home_team, spt_away_team, spt_time, percent)
                        bcl_df = sort_by_name_and_time_exact(bcl_df_f, spt_home_team, spt_away_team, spt_time, percent)
                        fst_df = sort_by_name_and_time_exact(fst_df_f, spt_home_team, spt_away_team, spt_time, percent)
                        frb_df = sort_by_name_and_time_exact(frb_df_f, spt_home_team, spt_away_team, spt_time, percent)
                        pre_df = sort_by_name_and_time_exact(pre_df_f, spt_home_team, spt_away_team, spt_time, percent)
                        sta_df = sort_by_name_and_time_exact(sta_df_f, spt_home_team, spt_away_team, spt_time, percent)

                        acc_df['weight'] = weights['ACC']
                        bcl_df['weight'] = weights['BCL']
                        fst_df['weight'] = weights['FST']
                        frb_df['weight'] = weights['FRB']
                        pre_df['weight'] = weights['PRE']
                        sta_df['weight'] = weights['STA']

                        all_df = [acc_df,bcl_df,fst_df,frb_df,pre_df,sta_df]
                        old_new_df = pd.concat(all_df, ignore_index=True)
                        new_df = old_new_df.drop_duplicates(subset=['NAME'],keep='first')

                        try:
                            cols_to_convert = ['HOME PER', 'DRAW PER', 'AWAY PER', 'OVER 2_5', 'UNDER 2_5', 'BTS', 'OTS']
                            for col in cols_to_convert:
                                new_df[col] = pd.to_numeric(new_df[col], errors='coerce')  # converts invalid entries to NaN
                            new_df['weight'] = pd.to_numeric(new_df['weight'], errors='coerce')
                            
                            frb_time = new_df['TIME'][0]
                            frb_home_team = new_df['HOME TEAM'][0]
                            frb_away_team = new_df['AWAY TEAM'][0]
                            frb_home_per = round((new_df['HOME PER'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
                            frb_draw_per = round((new_df['DRAW PER'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
                            frb_away_per = round((new_df['AWAY PER'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
                            frb_ovr25_per = round((new_df['OVER 2_5'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
                            frb_und25_per = round((new_df['UNDER 2_5'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
                            frb_bts_per = round((new_df['BTS'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
                            frb_ots_per = round((new_df['OTS'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
                            print(f'LEN_DF:{len(new_df)} (H:{frb_home_per}) (D:{frb_draw_per}) A:({frb_away_per}) (OV:{frb_ovr25_per}) (UN:{frb_und25_per}) (BTS:{frb_bts_per}) (OTS:{frb_ots_per}) \n')
                        except:
                            frb_home_per = 0
                            frb_draw_per = 0
                            frb_away_per = 0
                            frb_ovr25_per = 0
                            frb_und25_per = 0
                            frb_bts_per = 0
                            frb_ots_per = 0

                        
                        print('==================== MATCHED DATA ====================== \n')
                        # print(new_df)                    

                        if len(new_df) >= agree_no and max(frb_home_per, frb_draw_per, frb_away_per) >=FA3W_percent and frb_ots_per >= other_check:
                            # ======================================  1 X 2 OPTIONS  ===============================================
                            print(' \n 1 X 2 DETECTED, CHECKING FOR EDGE ODDS NOW....')
                            click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]')
                            click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]')

                            if frb_home_per >= FA3W_percent:
                                try:
                                    spt_hodd =  page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[1]')
                                    spt_hodd_text = spt_hodd.text_content().strip()
                                    home_edge = cal(float(spt_hodd_text), frb_home_per)
                                    if home_edge >= A_edge:
                                        time.sleep(1.5)
                                        click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[1]')
                                        place_bet(page, home_edge)
                                        print(f'\n PLACED BET ON >>>>> (HOME EDGE : {home_edge} %  @ {spt_hodd_text} WITH ACCU : {frb_home_per}% ) \n')
                                    print(f'HOME EDGE : {home_edge} %  @ {spt_hodd_text} WITH ACCU : {frb_home_per}% \n')
                                except Exception as e:
                                    print(f"Error fetching home odd: {e}")
                            
                            if frb_draw_per >= FA3W_percent:
                                try:
                                    spt_dodd =  page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[2]')
                                    spt_dodd_text = spt_dodd.text_content().strip()
                                    draw_edge = cal(float(spt_dodd_text), frb_draw_per)
                                    if draw_edge >= A_edge:
                                        time.sleep(1.5)
                                        click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[2]')
                                        place_bet(page, draw_edge)
                                        print(f'\n PLACED BET ON >>>>> (DRAW EDGE : {draw_edge} %  @ {spt_dodd_text} WITH ACCU : {frb_draw_per}% ) \n')
                                    print(f'DRAW EDGE : {draw_edge} %  @ {spt_dodd_text} WITH ACCU : {frb_draw_per}% \n')
                                except Exception as e:
                                    print(f"Error fetching draw odd: {e}")


                            if frb_away_per >= FA3W_percent:
                                try:
                                    spt_aodd =  page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[3]')
                                    spt_aodd_text = spt_aodd.text_content().strip()
                                    away_edge = cal(float(spt_aodd_text), frb_away_per)
                                    if away_edge >= A_edge:
                                        time.sleep(1.5)
                                        click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[1]/div[3]')
                                        place_bet(page, away_edge)
                                        print(f'\n PLACED BET ON >>>>> (AWAY EDGE : {away_edge} %  @ {spt_aodd_text} WITH ACCU : {frb_away_per}% ) \n')
                                    print(f'AWAY EDGE : {away_edge} %  @ {spt_aodd_text} WITH ACCU : {frb_away_per}% \n')
                                except Exception as e:
                                    print(f"Error fetching away odd: {e}")



                        if len(new_df) >= agree_no and max(frb_ovr25_per, frb_und25_per) >= FA_OVRUND_percent:
                            # ======================================== Over/Under 2.5 OPTIONS ================================================
                            click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]')
                            click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[1]')
                            print(' \n CLICKING ON OVER/UNDER 2.5 OPTION NOW....')
                            xpath = f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[1]'
                            try:
                                locator = page.locator(f"xpath={xpath}")

                                if locator.count() > 0:
                                    locator.first.click()
                                    time.sleep(1)  # allow dropdown animation
                                else:
                                    pass

                                page.wait_for_selector('.af-select-list-open', state="visible", timeout=6000)    
                                page.evaluate("""
                                    () => {
                                        const options = document.querySelectorAll('.af-select-list-open .af-select-item');
                                        for (let opt of options) {
                                            if (opt.textContent.trim() === '2.5') {
                                                opt.click();
                                                break;
                                            }
                                        }
                                    }
                                """)

                            except:
                                print('\n MAYBE OVR/UND 2.5 SELECTION DOESNT EXIST \n')

                            try:
                                main_ovr_odd =  page.wait_for_selector(xpath, timeout=Err_Timeout)
                                main_ovr_odd_text = main_ovr_odd.text_content().strip()
                            except:
                                main_ovr_odd_text = '5.5'
                                
                            if '2.5' in main_ovr_odd_text:
                                print('OVER / UNDER 2.5 DETECTED, CHECKING FOR EDGE ODDS NOW....')
                                time.sleep(1)
                                if frb_ovr25_per >= FA_OVRUND_percent and frb_bts_per >= other_check :
                                    try:
                                        spt_ovr_odd =  page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[2]')
                                        spt_ovr_odd_text = spt_ovr_odd.text_content().strip()
                                        over_edge = cal(float(spt_ovr_odd_text), frb_ovr25_per)
                                        if over_edge >= A_edge:
                                            time.sleep(1.5)
                                            click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[2]')
                                            place_bet(page, over_edge)
                                            print(f'\n PLACED BET ON >>>>> (OVER 2.5 EDGE : {over_edge} %  @ {spt_ovr_odd_text} WITH ACCU : {frb_ovr25_per}% ) \n')
                                        print(f'OVER 2.5 EDGE : {over_edge} %  @ {spt_ovr_odd_text} WITH ACCU : {frb_ovr25_per}% \n')
                                    except Exception as e:
                                        print(f"Error fetching over odd: {e}")

                                if frb_und25_per >= FA_OVRUND_percent and frb_ots_per >= other_check:
                                    try:
                                        spt_und_odd =  page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[3]')
                                        spt_und_odd_text = spt_und_odd.text_content().strip()
                                        under_edge = cal(float(spt_und_odd_text), frb_und25_per)
                                        if under_edge >= A_edge:
                                            time.sleep(1.5)
                                            click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div[2]/div[3]')
                                            place_bet(page, under_edge)
                                            print(f'\n PLACED BET ON >>>>> (UNDER 2.5 EDGE : {under_edge} %  @ {spt_und_odd_text} WITH ACCU : {frb_und25_per}% ) \n')
                                        print(f'UNDER 2.5 EDGE : {under_edge} %  @ {spt_und_odd_text} WITH ACCU : {frb_und25_per}% \n')
                                    except Exception as e:
                                        print(f"Error fetching under odd: {e}")



                        if len(new_df) >= agree_no and max(frb_bts_per, frb_ots_per) >= FA_BTTS_percent:
                            # # =====================================     BTS / OTS OPTIONS   ============================================
                            print(' \n CLICKING ON BTS/OTS OPTION NOW....')
                            click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[3]')
                            click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[3]/div[3]')

                            if frb_bts_per >= FA_BTTS_percent and frb_ovr25_per >= other_check:
                                try:
                                    spt_bts_odd =  page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div/div[1]')
                                    spt_bts_odd_text = spt_bts_odd.text_content().strip()
                                    bts_edge = cal(float(spt_bts_odd_text), frb_bts_per)
                                    if bts_edge >= A_edge:
                                        time.sleep(1.5)
                                        click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div/div[1]')
                                        place_bet(page, bts_edge) 
                                        print(f'\n PLACED BET ON >>>>> (BOTH TEAMS TO SCORE EDGE : {bts_edge} %  @ {spt_bts_odd_text} WITH ACCU : {frb_bts_per}% ) \n')
                                    print(f'BOTH TEAMS TO SCORE EDGE : {bts_edge} %  @ {spt_bts_odd_text} WITH ACCU : {frb_bts_per}% \n')
                                except Exception as e:
                                    print(f"Error fetching BTS odd: {e}")

                            if frb_ots_per >= FA_BTTS_percent and frb_und25_per >= other_check:
                                try:
                                    spt_ots_odd =  page.wait_for_selector(f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div/div[2]')
                                    spt_ots_odd_text = spt_ots_odd.text_content().strip()
                                    ots_edge = cal(float(spt_ots_odd_text), frb_ots_per)
                                    if ots_edge >= A_edge:    
                                        time.sleep(1.5)
                                        click_center(page, f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[2]/div/div[2]')
                                        place_bet(page, ots_edge)
                                        print(f'\n PLACED BET ON >>>>> (OTS SCORE EDGE : {ots_edge} %  @ {spt_ots_odd_text} WITH ACCU : {frb_ots_per}% ) \n')
                                    print(f'OTS SCORE EDGE : {ots_edge} %  @ {spt_ots_odd_text} WITH ACCU : {frb_ots_per}% \n')
                                except Exception as e:
                                    print(f"Error fetching OTS odd: {e}")
                firebase_read_and_save(data=pp_data,file_name='PLAYED_MATCHES')
                                        
    
        browser.close()

SportyBet_func()