import base64
import requests
import time
from pathlib import Path
import json 

from scripts.messages import get_message

def base64_to_audio(base64_string, file_path):
    binary_data = base64.b64decode(base64_string)

    with open(file_path, 'wb') as f:
        f.write(binary_data)
        
    print(f"File saved to {file_path}")

def text_to_audio(text, output):
    if not Path(output).parent.exists():
        Path(output).parent.mkdir(parents=True, exist_ok=True)
    
    response = requests.post("https://tiktok-tts.weilnet.workers.dev/api/generation", json={'text': text, 'voice': 'en_us_001'})
    error_message = "Something went wrong with the tiktok api"
    if response.status_code != 200:
        raise Exception(error_message)

    data = response.json()

    if not data['success']:
        raise Exception(error_message)

    base64_to_audio(data['data'], output);

def save_messages_to_file(messages, id):
    if not Path(f"assets/temp/{id}/audio").exists():
        Path(f"assets/temp/{id}/audio").mkdir(parents=True, exist_ok=True)

    with open(f"assets/temp/{id}/audio/messages.json", 'w') as outfile:
        json.dump(messages, outfile)

def generate_audio_messages(coinValues, input, id):
    payload = {
        **input,
        **coinValues
    }

    messages = get_message(payload)

    save_messages_to_file(messages, id)

    for i, message in enumerate(messages):
        text_to_audio(message, f"assets/temp/{id}/audio/audio-{i + 1}.wav")
        time.sleep(3)


