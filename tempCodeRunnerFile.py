# 截取整个网页的示例（Python版）
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    print('wait...')
    page.goto("https://qcc.com/login", wait_until="networkidle")
    print('ready...')
    page.screenshot(path="screenshots/login_page.png", full_page=True)
    print('fin!')
    browser.close()
    print('closed!')
