
from difflib import SequenceMatcher as ss
from datetime import datetime, timedelta
from datetime import date, timedelta
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import requests
import atexit
import time
import os

 
match_day_date = 0

def main_date(day = match_day_date):
    last_date = date.today() + timedelta(day)
    return last_date

def info_init():
    url = "https://trying-20541-default-rtdb.firebaseio.com/Main_info.json"
    response = requests.get(url)
    data = response.json()['main_init']
    print(data)
info_init()


def save_daily_csv():
    outcome_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'CSV FILES')
    todays_dir = str(main_date(match_day_date))+' Files'
    full_path = os.path.join(outcome_dir,todays_dir)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path
    
    
def save_daily_csv2(main_dir,second_dir_path_name):
    outcome_dir = main_dir
    todays_dir = second_dir_path_name
    full_path = os.path.join(outcome_dir,todays_dir)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path
    

def requests_init(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content,"html.parser")
    tree = html.fromstring(res.content)
    return soup,tree


def tree_init(optional):
    tree = html.fromstring(optional)


def saving_to_firebase(data,file_name):
    todays_date = datetime.now().strftime("%Y-%m-%d")
    try:
        clean_data = {}
        clean_data_to = data.to_dict(orient="list")  # list of row dicts
        for key, value in clean_data_to.items():
            new_key = key.replace(".", "_")
            clean_data[new_key] = value
    except:
        clean_data = {}
        for key, value in data.items():
            new_key = key.replace(".", "_")
            clean_data[new_key] = value
    firebase_url = f"https://kelly-football-dataset-default-rtdb.firebaseio.com/CSV_FILE/{todays_date}/{file_name}.json"
    response = requests.put(firebase_url, json=clean_data)
    print(response.status_code)
    print('\n FILE SAVED FOR THE NAME OF:',file_name,'\n')


def reading_firebase_csv(file_name):
    todays_date = datetime.now().strftime("%Y-%m-%d")
    firebase_url = f"https://kelly-football-dataset-default-rtdb.firebaseio.com/CSV_FILE/{todays_date}/{file_name}.json"
    response = requests.get(firebase_url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

def firebase_read_and_save(data, file_name):
    df = reading_firebase_csv(file_name)
    if len(df) == 0:
        saving_to_firebase(data, file_name)
    else:
        new_df = pd.DataFrame(data)
        combined_df = pd.concat([df, new_df], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['INFO'], keep='first')
        saving_to_firebase(combined_df, file_name)
        

def saving_files(data,path):
    df = pd.DataFrame(data)
    print(df.to_string())

    try:
        df2 = pd.read_csv(path)
        all_df = pd.concat([df2, df], ignore_index=True)
        all_df.to_csv(path, index=False)
        print(' ------------------------------------ ALL FILES SAVED  ------------------------------------- \n \n')

    except:
        df.to_csv(path, index=False)
        print('============================= SECOND FILE SAVED ==========================')



def drop_duplicate(path):
    all_df = pd.read_csv(path)
    all_df = all_df.drop_duplicates(subset=['HOME TEAM'],keep='first')
    all_df = all_df.reset_index()
    all_df.drop(['index'], axis=1, inplace=True)
    all_df.to_csv(path, index=False)


def sorting_values(path,value,ascending_mode):
    df = pd.read_csv(path)
    df = df.sort_values(by=value,ascending=ascending_mode)
    df.to_csv(path, index=False)


def sorting_values_path_to_save(path,value,path_to_save,ascending_mode):
    df = pd.read_csv(path)
    df = df.sort_values(by=value,ascending=ascending_mode)
    df.to_csv(path_to_save, index=False)



def place_bet(page, edge_amt, browser_delay_time=5000, main_amt=100):
    amt_to_bet = round((edge_amt * main_amt) + 5)
    page.on("dialog", lambda dialog: dialog.dismiss())
    input_element = page.wait_for_selector('#j_stake_0 input', timeout=browser_delay_time)
    page.eval_on_selector(
        '#j_stake_0 input',
        "el => el.scrollIntoView({behavior:'smooth', block:'center'})")

    input_element.click()
    time.sleep(1)
    input_element.click()
    time.sleep(1)

    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    time.sleep(1)

    # Type stake amount
    input_element.fill(str(amt_to_bet))
    time.sleep(2)

    try:
        odd_changes = page.wait_for_selector(
            'xpath=//button[contains(@class, "af-button--primary")]//span[text()="Accept Changes"]',
            timeout=2000)
        odd_changes.click()
        time.sleep(2)
        odd_changes.click()

    except:
        pass

    place_bet_element = page.wait_for_selector(
        'xpath=//button[.//span[@data-cms-key="place_bet" and @data-cms-page="component_betslip" and normalize-space(text())="Place Bet"]]'
    )

    page.eval_on_selector(
        'xpath=//button[.//span[@data-cms-key="place_bet" and @data-cms-page="component_betslip"]]',
        "el => el.scrollIntoView({behavior:'smooth', block:'center'})"
    )

    time.sleep(1)

    place_bet_element.click()
    time.sleep(1.5)

    place_bet_element.click()
    time.sleep(1.5)

    confirm_button = page.wait_for_selector(
        'xpath=//button[.//span[@data-cms-key="confirm" and @data-cms-page="common_functions"]]')

    confirm_button.click()
    time.sleep(2)

    # Click OK
    ok_button = page.wait_for_selector(
        'xpath=//button[@data-action="close" and @data-ret="close" and .//span[@data-cms-key="ok" and @data-cms-page="common_functions"]]'
    )
    ok_button.click()
    time.sleep(1)




def click_center(page, xpath: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for element to appear
        page.wait_for_selector(f"xpath={xpath}", state="visible", timeout=8000)

        # 2️⃣ Get element handle
        elements = page.locator(f"xpath={xpath}")

        if elements.count() == 0:
            print(f"[WARNING] Element not found: {xpath}")
            return False

        element = elements.first

        # 3️⃣ Scroll element to center
        element.evaluate("""
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        """)

        time.sleep(1)
        time.sleep(delay)

        # 4️⃣ Get bounding box
        box = element.bounding_box()

        if not box:
            print(f"[WARNING] Element '{xpath}' not visible or has no bounding box.")
            return False

        # 5️⃣ Calculate center
        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] / 2

        # 6️⃣ Click center
        time.sleep(1)
        page.mouse.click(x, y)

        print(f"[OK] Clicked center of '{xpath}' at ({x:.2f}, {y:.2f})")

        return True

    except Exception as e:
        print(f"[ERROR] Could not click on '{xpath}': {e}")
        return False
    


def sort_by_name_and_time_exact(df, spt_home_team, spt_away_team, spt_time, percent):
    try:
        # Step 1: Calculate similarity for home team
        df['HOME_SIMILARITY'] = df['HOME TEAM'].apply(
            lambda x: ss(None, str(x).lower(), str(spt_home_team).lower()).ratio() * 100
        )

        # Step 2: Calculate similarity for away team
        df['AWAY_SIMILARITY'] = df['AWAY TEAM'].apply(
            lambda x: ss(None, str(x).lower(), str(spt_away_team).lower()).ratio() * 100
        )

        # Step 3: Keep rows where both similarities >= threshold
        filtered_df = df[
            (df['HOME_SIMILARITY'] >= percent) &
            (df['AWAY_SIMILARITY'] >= percent)
        ].copy()

        if filtered_df.empty:
            return filtered_df  # nothing matches, return empty

        # Step 4: Sort by combined similarity
        filtered_df['TOTAL_SIMILARITY'] = (
            filtered_df['HOME_SIMILARITY'] + filtered_df['AWAY_SIMILARITY']
        ) / 2
        filtered_df = filtered_df.sort_values(by='TOTAL_SIMILARITY', ascending=False).reset_index(drop=True)

        # Step 5: Filter by exact times (1 hour before, same hour, and 1 hour after)
        spt_time_dt = datetime.strptime(spt_time, "%H:%M")

        valid_times = {
            (spt_time_dt - timedelta(hours=1)).strftime("%H:%M"),  # 1 hour before
            spt_time_dt.strftime("%H:%M"),                         # exact time
            (spt_time_dt + timedelta(hours=1)).strftime("%H:%M")   # 1 hour after
        }

        filtered_df = filtered_df[filtered_df['TIME'].isin(valid_times)].reset_index(drop=True)

        # Step 6: Drop helper columns
        filtered_df = filtered_df.drop(columns=['HOME_SIMILARITY', 'AWAY_SIMILARITY', 'TOTAL_SIMILARITY'])

        return filtered_df

    except Exception as e:
        print(f"Error sorting by team similarity and time: {e}")
        return df




def xpath_scroll_center(page, xpath: str, delay: float = 0.5):
    try:
        # 1️⃣ Wait for element to appear
        page.wait_for_selector(f"xpath={xpath}", state="visible", timeout=10000)

        # 2️⃣ Get element
        locator = page.locator(f"xpath={xpath}")

        if locator.count() == 0:
            print(f"[WARNING] Element not found: {xpath}")
            return False

        element = locator.first

        # 3️⃣ Scroll element to center
        element.evaluate("""
            (element) => {
                element.scrollIntoView({
                    behavior: "smooth",
                    block: "center",
                    inline: "center"
                });
            }
        """)

        print(f"[OK] Scrolled To center of '{xpath}'")

        return True

    except Exception as e:
        print(f"[ERROR] Could not scroll on '{xpath}': {e}")
        return False


atexit.register(info_init)