# 截取整个网页的示例（Python版）
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    print('Starting...')
    page.goto("https://qcc.com/login", wait_until="networkidle")
    page.screenshot(path="screenshots/login_page.png", full_page=True)
    print('Finished!')
    browser.close()
