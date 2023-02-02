from playwright.sync_api import sync_playwright, ViewportSize
import time
import urllib.parse

from config import dca_cc_host


def execute_playwright(coin, id):
    with sync_playwright() as p:
        print("Launching browser...")

        browser = p.chromium.launch(slow_mo=50)
        context = browser.new_context(storage_state="auth.json", viewport=ViewportSize(width=390, height=844))

        page = context.new_page()

        query_param_string = urllib.parse.urlencode(coin)

        url_string = f"{dca_cc_host}/dca/{coin['coinId']}?{query_param_string}"

        page.goto(url_string)

        time.sleep(5)

        print(url_string)
        

        # Take screenshots
        # "Get in on the Bitcoin action!",
        page.screenshot(path=f"assets/temp/{id}/png/screenshot-1.png")

        # "Today Bitcoin hits a price of $24,017!",
        page.get_by_test_id("coin-today-price").screenshot(path=f"assets/temp/{id}/png/screenshot-2.png")

        # "If you invested 10 every month for 3 years",
        page.get_by_test_id("button-open-change-params").click()
        page.get_by_test_id("change-params-form").screenshot(path=f"assets/temp/{id}/png/screenshot-3.png")
        page.get_by_test_id("button-close-change-params").click()
        time.sleep(2)

        # "You would have invested $370 in total",
        page.get_by_test_id("total-investment").screenshot(path=f"assets/temp/{id}/png/screenshot-4.png")
        
        # "Today, this would be worth $414.04!",
        page.get_by_test_id("value-in-fiat").screenshot(path=f"assets/temp/{id}/png/screenshot-5.png")

        # "DCA - turns $370 into $414.04 in 3 years!",
        page.screenshot(path=f"assets/temp/{id}/png/screenshot-6.png")

        # "To see more, visit dca-cc.com for more backtesting!"
        page.evaluate("() => window.scrollTo(0, 0)")
        time.sleep(1)
        page.screenshot(path=f"assets/temp/{id}/png/screenshot-7.png")

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
