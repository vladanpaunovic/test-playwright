from scripts.playwright_scripts import execute_playwright
from scripts.record_audio import generate_audio_messages
from scripts.video.background import prepare_video
from scripts.video.final_video import make_final_video
from config import dca_cc_api
from uuid import uuid4
from datetime import datetime

import requests


def get_chart_data_from_dca_api():
    response = requests.post(f"{dca_cc_api}/social/content")
    return response.json()

def create_video_id():
    uuid_str = str(uuid4()).replace("-", "")[:8]
    return datetime.now().strftime('%Y-%m-%d_%H:%M:%S___') + uuid_str


def main():
    # Get data
    response = get_chart_data_from_dca_api()

    id = create_video_id()

    print("Video ID:", id)

    # Take screenshots
    coinValues = execute_playwright(response["payload"], id)

    # Record audio
    generate_audio_messages(coinValues, response, id)

    # Combine audio and video
    background_clip, bg_config = prepare_video(id)

    # Write video
    make_final_video(background_clip, id, bg_config)
    
    print("Done.")



if __name__ == "__main__":
    main()