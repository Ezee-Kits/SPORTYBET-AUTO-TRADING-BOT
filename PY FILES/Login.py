
import time



def Login_to(page):
    print("\n>>> NOT LOGGED IN! PROCEEDING TO LOGIN... <<<\n")

    email_to_input = ''  # Enter email/phone number here
    password_to_input = ''  # Enter password here

    # Use locators instead of ElementHandle
    email_input = page.locator('div.m-phone input[name="phone"]')
    password_input = page.locator('div.m-psd input[name="psd"]')
    login_button = page.locator('button[name="logIn"]')

    # Type email/phone
    email_input.scroll_into_view_if_needed()
    email_input.click(timeout=50000)
    email_input.fill(str(email_to_input), timeout=50000)

    # Type password
    password_input.scroll_into_view_if_needed()
    password_input.click(timeout=5000)
    password_input.fill(str(password_to_input), timeout=50000)

    # Click login
    login_button.scroll_into_view_if_needed()
    login_button.click(timeout=50000)
    login_button.click(timeout=50000)

    # Wait for balance element to confirm login
    now_balance = page.locator('span[id="j_balance"]')
    try:
        now_balance.wait_for(state="visible", timeout=50000)
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



# def Login_to(page):

#     print("\n>>> NOT LOGGED IN! PROCEEDING TO LOGIN... <<<\n")

#     email_to_input = '9027794130' #input("Enter phone number:::::::: ")
#     password_to_input = 'Goldenpenny2pussy' #input("Enter password:::::::: ")

#     email_to = page.wait_for_selector('div.m-phone input[name="phone"]', timeout=50000)

#     page.eval_on_selector(
#         'div.m-phone input[name="phone"]',
#         "el => el.scrollIntoView({behavior:'smooth', block:'center'})"
#     )

#     email_to.click()
#     time.sleep(1)

#     email_to.click()
#     time.sleep(1)

#     page.keyboard.press("Control+A")
#     page.keyboard.press("Backspace")
#     time.sleep(1)

#     # Type phone number
#     email_to.fill(str(email_to_input))
#     time.sleep(1)


#     password_to = page.wait_for_selector('div.m-psd input[name="psd"]', timeout=50000)

#     page.eval_on_selector(
#         'div.m-psd input[name="psd"]',
#         "el => el.scrollIntoView({behavior:'smooth', block:'center'})"
#     )

#     password_to.click()
#     time.sleep(1)

#     password_to.click()
#     time.sleep(1)

#     page.keyboard.press("Control+A")
#     page.keyboard.press("Backspace")
#     time.sleep(1)

#     # Type password
#     password_to.fill(str(password_to_input))
#     time.sleep(1)


#     login_btn = page.wait_for_selector('button[name="logIn"]', timeout=50000)

#     page.eval_on_selector(
#         'button[name="logIn"]',
#         "el => el.scrollIntoView({behavior:'smooth', block:'center'})"
#     )

#     login_btn.click()
#     time.sleep(0.5)

#     login_btn.click()
#     time.sleep(2)


#     now_balance = page.wait_for_selector('span[id="j_balance"]', timeout=50000)

#     try:
#         balance_text = now_balance.text_content()
#         spt_acct_balance = int(
#             balance_text.strip()
#             .replace('NGN ', '')
#             .replace(',', '')
#             .split('.')[0]
#         )
#     except:
#         spt_acct_balance = None


#     if spt_acct_balance:
#         print(f"\n>>> ALREADY LOGGED IN! ACCOUNT BALANCE: {spt_acct_balance} <<<\n")
#     else:
#         input("PRESS ENTER AFTER LOGGING IN AND SETTING UP THE PAGE TO AUTOMATE...")

