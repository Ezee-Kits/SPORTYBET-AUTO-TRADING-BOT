from playwright.sync_api import sync_playwright
from datetime import datetime
import random

import time




def Login_to(page):

    print("\n>>> NOT LOGGED IN! PROCEEDING TO LOGIN... <<<\n")

    email_to_input = '9027794130' #input("Enter phone number:::::::: ")
    password_to_input = 'Goldenpenny2pussy' #input("Enter password:::::::: ")

    email_to = page.wait_for_selector('div.m-phone input[name="phone"]', timeout=15000)

    page.eval_on_selector(
        'div.m-phone input[name="phone"]',
        "el => el.scrollIntoView({behavior:'smooth', block:'center'})"
    )

    email_to.click()
    time.sleep(1)

    email_to.click()
    time.sleep(1)

    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    time.sleep(1)

    # Type phone number
    email_to.fill(str(email_to_input))
    time.sleep(1)


    password_to = page.wait_for_selector('div.m-psd input[name="psd"]', timeout=4000)

    page.eval_on_selector(
        'div.m-psd input[name="psd"]',
        "el => el.scrollIntoView({behavior:'smooth', block:'center'})"
    )

    password_to.click()
    time.sleep(1)

    password_to.click()
    time.sleep(1)

    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    time.sleep(1)

    # Type password
    password_to.fill(str(password_to_input))
    time.sleep(1)


    login_btn = page.wait_for_selector('button[name="logIn"]', timeout=4000)

    page.eval_on_selector(
        'button[name="logIn"]',
        "el => el.scrollIntoView({behavior:'smooth', block:'center'})"
    )

    login_btn.click()
    time.sleep(0.5)

    login_btn.click()
    time.sleep(2)


    now_balance = page.wait_for_selector('span[id="j_balance"]', timeout=15000)

    try:
        balance_text = now_balance.text_content()
        spt_acct_balance = int(
            balance_text.strip()
            .replace('NGN ', '')
            .replace(',', '')
            .split('.')[0]
        )
    except:
        spt_acct_balance = None


    if spt_acct_balance:
        print(f"\n>>> ALREADY LOGGED IN! ACCOUNT BALANCE: {spt_acct_balance} <<<\n")
    else:
        input("PRESS ENTER AFTER LOGGING IN AND SETTING UP THE PAGE TO AUTOMATE...")



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

    print('currently trying to search the url now')
    page.goto("https://www.sportybet.com/ng/sport/football/today", wait_until="networkidle")

    print(page.title())
    # Login_to(page)
    fir_match = 2
    sec_match = 2
    Err_Timeout = 3500  # WEBPAGE TIMEOUT

    print('currently on data extraction')

    try:
        date_elem = page.wait_for_selector(
            f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[1]/div[1]',
            timeout=Err_Timeout
        )
        spt_date = date_elem.text_content().split()[0]
        spt_date = datetime.strptime(f"2025/{spt_date}", "%Y/%d/%m").strftime("%Y-%m-%d")

        time_elem = page.wait_for_selector(
            f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[1]/div[1]',
            timeout=Err_Timeout
        )
        spt_time = time_elem.text_content().strip()

        home_elem = page.wait_for_selector(
            f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[1]',
            timeout=Err_Timeout
        )
        spt_home_team = home_elem.text_content().strip().replace('SRL','SIMULATED REALITY LEAGUE')

        away_elem = page.wait_for_selector(
            f'//*[@id="importMatch"]/div[{fir_match}]/div/div[4]/div[{sec_match}]/div[1]/div/div[2]/div[2]',
            timeout=Err_Timeout
        )
        spt_away_team = away_elem.text_content().strip().replace('SRL','SIMULATED REALITY LEAGUE')

    except:
        print('error on data extraction section')
        

    print(spt_date, spt_time, spt_home_team, spt_away_team)
    browser.close()




# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
    
#     browser = p.chromium.connect(f"wss://production-sfo.browserless.io/chromium/playwright?token=2U5Z09he7iz5ILvf3c59ccfe0957e415f3bff6325586faa9c")
#     page = browser.new_page()


#     page.goto("https://www.sportybet.com/ng/sport/football/today")

#     screenshot = page.screenshot()
#     print(f"Screenshot taken! Size: {len(screenshot)} bytes")
#     print(page.title())

#     browser.close()


