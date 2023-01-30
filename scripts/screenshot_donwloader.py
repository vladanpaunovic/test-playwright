from playwright.sync_api import sync_playwright, ViewportSize
import time
import urllib.parse

from config import dca_cc_host

def get_screenshots_dca(coin):
    test_ids = [
        "earnings-over-time",
        "coin-today-price",
        "top-cards"
    ]

    with sync_playwright() as p:
        print("Launching browser...")

        browser = p.chromium.launch(slow_mo=50)
        context = browser.new_context(storage_state="auth.json", viewport=ViewportSize(width=390, height=844))

        page = context.new_page()

        query_param_string = urllib.parse.urlencode(coin)

        url_string = f"{dca_cc_host}/dca/{coin['coinId']}?{query_param_string}"

        page.goto(url_string)

        current_coin_price = page.get_by_test_id("current-coin-price")

        time.sleep(5)

        for test_id in test_ids:
            page.get_by_test_id(test_id).screenshot(path=f"screenshots/{test_id}.png")
            print(f"Screenshot taken for {test_id}.")

        print("Screenshots taken.")

        return current_coin_price.inner_text()
