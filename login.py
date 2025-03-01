from playwright.sync_api import sync_playwright
import os
import json

os.makedirs("cookies", exist_ok=True)
if not os.path.exists("cookies/cookies.json"):
    with open("cookies/cookies.json", "w") as f:
        json.dump({}, f)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--window-position=-3200000,-3200000"]
    )
    context = browser.new_context(
        storage_state="cookies/cookies.json")
    page = context.new_page()
    print('Starting...')
    page.goto("https://www.qcc.com/404",
              wait_until="networkidle")
    page.screenshot(path="screenshots/login_page.png", full_page=True)
    print('Login QRCode Generated. Please rerun the program if it is no longer valid.')
    page.wait_for_url("https://www.qcc.com/404", timeout=0)
    print('Finished!')
    page.context.storage_state(path="cookies/cookies.json")
    browser.close()
