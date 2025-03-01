from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--window-position=-3200000,-3200000"]
    )  # 无头模式会被检测，因此我们将浏览器放置在远离屏幕的坐标位置，以简单地实现能隐藏浏览器窗口的“有头”状态。
    page = browser.new_page()
    print('Starting...')
    page.goto("https://www.qcc.com/weblogin?back=%2F404",
              wait_until="networkidle")
    page.screenshot(path="screenshots/login_page.png", full_page=True)
    page.wait_for_url("https://www.qcc.com/404")
    print('Finished!')
    page.context.storage_state(path="cookies/cookies.json")
    browser.close()
