import base64
import requests
from config import dca_cc_api

def base64_to_audio(base64_string, file_path):
    binary_data = base64.b64decode(base64_string)

    with open(file_path, 'wb') as f:
        f.write(binary_data)
        
    print(f"File saved to {file_path}")

def get_price_from_dca_api(coin_id):
    response = requests.post(f"{dca_cc_api}/coins/price/{coin_id}")
    return response.json()

def generate_text_message(payload):
    message = [
        f"🔥 Hot off the charts, today {payload['rawData']['coinName']} hits a price of {payload['currentPrice']}!",
        "🚀 Small steps lead to big wins!",
        f"Investing ${payload['rawData']['investment']} every {payload['rawData']['intervalLabel']} for {payload['rawData']['years']} years turns into ${int(payload['rawData']['totalValueFiat'])} out of only ${payload['rawData']['totalInvestment']} invested!",
        f"🔥 Want to maximize your investments? Head out to dca-cc.com to see where a ${payload['rawData']['dcaPercentageChange']} gains are coming from!",
    ]
    return message

def text_to_audio(text, output):
    response = requests.post("https://tiktok-tts.weilnet.workers.dev/api/generation", json={'text': text, 'voice': 'en_us_001'})
    error_message = "Something went wrong with the tiktok api"
    if response.status_code != 200:
        raise Exception(error_message)

    data = response.json()

    if not data['success']:
        raise Exception(error_message)

    base64_to_audio(data['data'], output);

def generate_audio_messages(response, currentPrice):
    payload = {
        **response,
        "currentPrice": currentPrice
    }

    messages = generate_text_message(payload)
    print(messages)

    for i, message in enumerate(messages):
        text_to_audio(message, f"./audio/{i+1}-audio.wav")

