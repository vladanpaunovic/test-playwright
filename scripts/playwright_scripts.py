from playwright.sync_api import sync_playwright, ViewportSize
import time
import urllib.parse

from config import dca_cc_host


def execute_playwright(coin, id):
    with sync_playwright() as p:
        print("Launching browser...")

        browser = p.chromium.launch(slow_mo=50, headless=False)
        context = browser.new_context(storage_state="auth.json", viewport=ViewportSize(width=390, height=844))

        page = context.new_page()

        query_param_string = urllib.parse.urlencode(coin)

        url_string = f"{dca_cc_host}/dca/{coin['coinId']}?{query_param_string}"

        page.goto(url_string)

        time.sleep(5)

        print(url_string)
        

        # Take screenshots

        # Today's price
        page.get_by_test_id("coin-today-price").screenshot(path=f"assets/temp/{id}/png/screenshot-1.png")
        
        # B roll
        page.screenshot(path=f"assets/temp/{id}/png/screenshot-2.png")


        # Investments tab
        page.get_by_test_id("button-open-change-params").click()
        page.get_by_test_id("change-params-form").screenshot(path=f"assets/temp/{id}/png/screenshot-3.png")
        page.get_by_test_id("button-close-change-params").click()
        time.sleep(2)
        
        # Charts
        page.get_by_test_id("value-in-fiat").screenshot(path=f"assets/temp/{id}/png/screenshot-4.png")
        
        # Earnings
        page.get_by_test_id("earnings-over-time").screenshot(path=f"assets/temp/{id}/png/screenshot-5.png")
        
        # CTA
        page.screenshot(path=f"assets/temp/{id}/png/screenshot-6.png")

        print("Screenshots taken.")

        # Get data
        values_test_ids = [
            "current-coin-price",
            "current-coin-value-in-fiat",
            "current-coin-total-investment",
            "current-coin-delta"
        ]

        data = {}
        for test_id_ in values_test_ids:
            data[test_id_] = page.get_by_test_id(test_id_).inner_text()

        return data
