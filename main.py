from scripts.screenshot_donwloader import get_screenshots_dca
from scripts.record_audio import generate_audio_messages
import requests
from config import dca_cc_api


def get_chart_data_from_dca_api():
    response = requests.post(f"{dca_cc_api}/social/content")
    return response.json()

def main():
    # Get data
    response = get_chart_data_from_dca_api()
    
    # Take screenshots
    currentPrice = get_screenshots_dca(response["payload"])

    # Record audio
    generate_audio_messages(response, currentPrice)

    # Combine audio and video


    print("Done.")


if __name__ == "__main__":
    main()