import random

def dca_hook(payload):
    hooks = [
        f"🔥 Hot off the charts, today {payload['rawData']['coinName']} hits a price of {payload['current-coin-price']}!",
        f"{payload['rawData']['coinName']} is heating up! Today, it hit a price of {payload['current-coin-price']} 🔥",
        f"Stay ahead of the game with {payload['rawData']['coinName']}! Today's price is {payload['current-coin-price']} 🔥",
        f"Get in on the {payload['rawData']['coinName']} action! Today's price reached {payload['current-coin-price']} 🔥",
        f"Don't miss out on {payload['rawData']['coinName']}! Today's price is {payload['current-coin-price']} 🔥",
    ]

    return random.choice(hooks)

def dca_earning(payload):
    story_lines_1 = [
        f"🚀 Small steps lead to big wins!",
        f"Take it slow and watch your investments grow 🚀",
        f"Baby steps lead to big gains 🚀",
        f"Wanna see a power of DCA? 🚀",
    ]
    
    concensus = [
        f"With just {payload['current-coin-total-investment']} invested, {payload['rawData']['years']} years of ${payload['rawData']['investment']} every {payload['rawData']['intervalLabel']} brought us {payload['current-coin-value-in-fiat']} 💰",
        f"Just ${payload['rawData']['investment']} every {payload['rawData']['intervalLabel']} for {payload['rawData']['years']} years, brought us {payload['current-coin-value-in-fiat']} 💰",
        f"Consistent investing with {payload['rawData']['investment']} every {payload['rawData']['intervalLabel']} for {payload['rawData']['years']} years brought us {payload['current-coin-value-in-fiat']} 💰",
        f"Investing smart with ${payload['rawData']['investment']} every {payload['rawData']['intervalLabel']}! {payload['current-coin-total-investment']} turned into {payload['current-coin-value-in-fiat']} in just {payload['rawData']['years']} years 💰",
    ]

    cta_hook = [
        f"🔥 Want to maximize your investments?",
        f"Investment success is just a click away!",
        f"🔥 Ready to boost your investment returns?",
        f"Discover the secret to investment success!",
    ]

    cta = [
        f"Head out to dca-cc.com to see where a {payload['current-coin-delta']} gains are coming from!",
        f"Visit dca-cc.com to see where the {payload['current-coin-delta']} profits are coming from 🔥",
        f"Check out dca-cc.com for the source of those {payload['current-coin-delta']} gains 🔥"
    ]

    message = [
        dca_hook(payload),
        random.choice(story_lines_1),
        f"DCA it to the max! Investing just ${payload['rawData']['investment']} brings big returns 💰",
        random.choice(concensus),
        random.choice(cta_hook),
        random.choice(cta),
    ]
    return message

def dca_losing(payload):
    message = [
        dca_hook(payload),
        "🚀 Small steps lead to big wins!",
        f"Let's DCA it - investing {payload['rawData']['investment']} every {payload['rawData']['intervalLabel']} for {payload['rawData']['years']} brings us what?",
        f"It's a {payload['current-coin-value-in-fiat']} out of {payload['current-coin-total-investment']} invested...",
        f"🔥 You are REKT!",
        f"Head out to dca-cc.com to see where a {payload['current-coin-delta']} losses are coming from!",
    ]
    return message


def is_earning(payload):
    delta = payload['current-coin-delta'].replace("$", "").replace(",", "")
    return float(delta) > 0

def get_message(payload):
    if is_earning(payload):
        output = dca_earning(payload)
    else:
        output = dca_losing(payload)

    return output