import random

# 1 Hot off the charts!
# 2 Today {coin} hits a price of {price}!

# 3 If you invested 10 dollars every week for 5 years
# 4 You would have invested 2600 dollars in total
# 5 Today, this would be worth 10000 dollars!
# 6 DCA - turns 2600 dollars into 10000 dollars in 5 years!

# 7 To see more, visit dca-cc.com for free backtesting!


def dca_hooks(payload):
    pre_hook = [
        f"🔥 Hot off the charts!",
        f"{payload['rawData']['coinName']} is heating up!",
        f"Stay ahead of the game with {payload['rawData']['coinName']}!",
        f"Get in on the {payload['rawData']['coinName']} action!",
        f"Don't miss out on {payload['rawData']['coinName']}!",
    ]

    price = [
        f"Today {payload['rawData']['coinName']} hits a price of {payload['current-coin-price']}!",
        f"Today, {payload['rawData']['coinName']} hit a price of {payload['current-coin-price']} 🔥",
        f"Today's {payload['rawData']['coinName']} price is {payload['current-coin-price']} 🔥",
        f"Today's {payload['rawData']['coinName']} price reached {payload['current-coin-price']} 🔥"
    ]

    return [
        random.choice(pre_hook), random.choice(price)
    ]

def dca_investing_payload(payload):
    value_in_fiat = float(payload['current-coin-value-in-fiat'].replace("$", "").replace(",", ""))
    
    messages = [
        f"If you invested ${payload['rawData']['investment']} every {payload['rawData']['intervalLabel']} for {payload['rawData']['years']} years",
        f"You would have invested {payload['current-coin-total-investment']} in total",
        f"Today, this would be worth ${round(value_in_fiat)}!",
    ]

    if is_earning(payload):
        messages.append(f"DCA - turns {payload['current-coin-total-investment']} into ${round(value_in_fiat)} in {payload['rawData']['years']} years!")
    else:
        price_difference = float(payload['current-coin-total-investment'].replace("$", "").replace(",", "")) - value_in_fiat
        messages.append(f"With DCA, you would lose ${round(price_difference)} in {payload['rawData']['years']} years")

    return messages

def dca_cta_string(payload):
    cta = [
        f"To see more, visit dca-cc.com for more backtesting!",
    ]

    # if is_earning(payload):
    #     cta.append(f"Head out to dca-cc.com to see where a {payload['current-coin-delta']} gains are coming from!")
    # else:
    #     cta.append(f"Head out to dca-cc.com to see where a {payload['current-coin-delta']} losses are coming from!")

    return random.choice(cta)


def is_earning(payload):
    delta = payload['current-coin-delta'].replace("$", "").replace(",", "")
    return float(delta) > 0

def get_message(payload):
    message = [
        *dca_hooks(payload),
        *dca_investing_payload(payload),
        dca_cta_string(payload)
    ]

    return message