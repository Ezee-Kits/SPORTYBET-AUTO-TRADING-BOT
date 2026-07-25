import pandas as pd
import requests
from datetime import datetime
from func import reading_firebase_csv,saving_to_firebase,sort_by_name_and_time_exact





# weights = {
#     'ACC': 0.8,  # Accumulator Generator
#     'BCL': 1.0,  # Betclan
#     'FST': 0.9,  # FootballSuperTips
#     'FRB': 1.4,  # Forebet
#     'PRE': 1.1,  # Prematips
#     'STA': 1.2   # Statarea
# }


# spt_home_team = 'Tottenham'
# spt_away_team = 'Crystal Palace'
# spt_time = '21:00'
# percent = 55

acc_df_f = reading_firebase_csv(file_name = 'Accumulator')
# bcl_df_f = reading_firebase_csv(file_name = 'Betclan')
# fst_df_f = reading_firebase_csv(file_name = 'Footballsupertips')
# frb_df_f = reading_firebase_csv(file_name = 'Forebet')
# pre_df_f = reading_firebase_csv(file_name = 'Prematips')
# sta_df_f = reading_firebase_csv(file_name = 'Statarea')
print(acc_df_f)
# # print(pre_df_f)
# # print(sta_df_f)

# acc_df = sort_by_name_and_time_exact(acc_df_f, spt_home_team, spt_away_team, spt_time, percent)
# bcl_df = sort_by_name_and_time_exact(bcl_df_f, spt_home_team, spt_away_team, spt_time, percent)
# fst_df = sort_by_name_and_time_exact(fst_df_f, spt_home_team, spt_away_team, spt_time, percent)
# frb_df = sort_by_name_and_time_exact(frb_df_f, spt_home_team, spt_away_team, spt_time, percent)
# pre_df = sort_by_name_and_time_exact(pre_df_f, spt_home_team, spt_away_team, spt_time, percent)
# sta_df = sort_by_name_and_time_exact(sta_df_f, spt_home_team, spt_away_team, spt_time, percent)





# acc_df['weight'] = weights['ACC']
# bcl_df['weight'] = weights['BCL']
# fst_df['weight'] = weights['FST']
# frb_df['weight'] = weights['FRB']
# pre_df['weight'] = weights['PRE']
# sta_df['weight'] = weights['STA']

# all_df = [acc_df,bcl_df,fst_df,frb_df,pre_df,sta_df]
# old_new_df = pd.concat(all_df, ignore_index=True)
# new_df = old_new_df.drop_duplicates(subset=['NAME'],keep='first')

# print(new_df)

# cols_to_convert = ['HOME PER', 'DRAW PER', 'AWAY PER', 'OVER 2_5', 'UNDER 2_5', 'BTS', 'OTS']
# for col in cols_to_convert:
#     new_df[col] = pd.to_numeric(new_df[col], errors='coerce')  # converts invalid entries to NaN
# new_df['weight'] = pd.to_numeric(new_df['weight'], errors='coerce')


# frb_time = new_df['TIME'][0]
# frb_home_team = new_df['HOME TEAM'][0]
# frb_away_team = new_df['AWAY TEAM'][0]
# frb_home_per = round((new_df['HOME PER'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
# frb_draw_per = round((new_df['DRAW PER'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
# frb_away_per = round((new_df['AWAY PER'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
# frb_ovr25_per = round((new_df['OVER 2_5'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
# frb_und25_per = round((new_df['UNDER 2_5'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
# frb_bts_per = round((new_df['BTS'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
# frb_ots_per = round((new_df['OTS'] * new_df['weight']).sum() / new_df['weight'].sum(), 2)
# print(f'LEN_DF:{len(new_df)} (H:{frb_home_per}) (D:{frb_draw_per}) A:({frb_away_per}) (OV:{frb_ovr25_per}) (UN:{frb_und25_per}) (BTS:{frb_bts_per}) (OTS:{frb_ots_per}) \n')








# pp_data = {'INFO':[]}
# pp_data['INFO'].append('2025-03-05 21:00 Tottenham Crystal Palace')


# try:
    # pp_data_df = reading_firebase_csv(file_name = 'PLAYED_MATCHES')
# except:
#     print('no data in the firebase for the played matches yet')
#     pp_data_df = pd.DataFrame({'INFO':['starting']})['INFO'].to_list()
#     print(pp_data_df)
#     saving_to_firebase(data=pp_data,file_name='PLAYED_MATCHES')



# pp_data_df = reading_firebase_csv(file_name = 'PLAYED_MATCHES')
# print(len(pp_data_df))

# from datetime import datetime, timedelta

# file_name = 'Accumulator'
# todays_date = datetime.now().strftime("%Y-%m-%d")
# firebase_url = f"https://kelly-football-dataset-default-rtdb.firebaseio.com/CSV_FILE/{todays_date}/{file_name}.json"
# response = requests.get(firebase_url)
# data = response.json()
# # Check how many items each key has
# for key, value in data.items():
#     if isinstance(value, list):
#         print(f"{key} → {len(value)} entries")
#     elif isinstance(value, dict):
#         print(f"{key} → {len(value)} entries")
#     else:
#         print(f"{key} → single value: {value}")



        
# df = pd.DataFrame(data)