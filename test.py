from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    print('Starting...')
    page.goto("https://www.qcc.com/weblogin?back=%2F404",
              wait_until="networkidle")
    page.screenshot(path="screenshots/login_page.png", full_page=True)
    print('Finished!')
    page.wait_for_url("https://qcc.com/404")
    browser.close()
