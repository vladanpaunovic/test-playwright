import json
import random

from pathlib import Path
from random import randrange
from typing import Any, Tuple

from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube
from pytube.cli import on_progress
from utils.console import print_step, print_substep
from scripts.video.final_video import make_audio, make_final_video

# Load background videos
with open("./scripts/video/backgrounds.json") as json_file:
    background_options = json.load(json_file)

def get_start_and_end_times(video_length: int, length_of_clip: int) -> Tuple[int, int]:
    """Generates a random interval of time to be used as the background of the video.

    Args:
        video_length (int): Length of the video
        length_of_clip (int): Length of the video to be used as the background

    Returns:
        tuple[int,int]: Start and end time of the randomized interval
    """
    random_time = randrange(180, int(length_of_clip) - int(video_length))
    return random_time, random_time + video_length


def get_background_config():
    choices = {
        "background_choice": {
            "default": "minecraft",
            "example": "rocket-league",
            "explanation": "Sets the background for the video based on game name",
            "optional": True,
            "options": [
                "minecraft",
                "gta",
                "rocket-league",
                "motor-gta",
                "csgo-surf",
                "cluster-truck",
                "minecraft-2",
                "multiversus",
                "fall-guys",
                "steep",
                ""
            ]
        }
    }
    """Fetch the background/s configuration"""
    try:
        choice = str(choices).casefold()
    except AttributeError:
        print_substep("No background selected. Picking random background'")
        choice = None

    # Handle default / not supported background using default option.
    # Default : pick random from supported background.
    if not choice or choice not in background_options:
        choice = random.choice(list(background_options.keys()))

    return background_options[choice]


def download_background(background_config: Tuple[str, str, str, Any]):
    """Downloads the background/s video from YouTube."""
    Path("./assets/backgrounds/").mkdir(parents=True, exist_ok=True)
    # note: make sure the file name doesn't include an - in it
    uri, filename, credit, _ = background_config
    if Path(f"assets/backgrounds/{credit}-{filename}").is_file():
        return
        
    print_step(
        "We need to download the backgrounds videos. they are fairly large but it's only done once. 😎"
    )
    print_substep("Downloading the backgrounds videos... please be patient 🙏 ")
    print_substep(f"Downloading {filename} from {uri}")
    
    YouTube(uri, on_progress_callback=on_progress).streams.filter(
        res="1080p"
    ).first().download("assets/backgrounds", filename=f"{credit}-{filename}")

    print_substep("Background video downloaded successfully! 🎉", style="bold green")


def chop_background_video(
    background_config: Tuple[str, str, str, Any], video_length: int, id: str
):
    """Generates the background footage to be used in the video and writes it to assets/temp/background.mp4

    Args:
        background_config (Tuple[str, str, str, Any]) : Current background configuration
        video_length (int): Length of the clip where the background footage is to be taken out of
    """

    print_step("Finding a spot in the backgrounds video to chop...✂️")
    choice = f"{background_config[2]}-{background_config[1]}"

    Path(f"assets/temp/{id}/").mkdir(parents=True, exist_ok=True)

    background = VideoFileClip(f"assets/backgrounds/{choice}")

    start_time, end_time = get_start_and_end_times(video_length, background.duration)
    try:
        ffmpeg_extract_subclip(
            f"assets/backgrounds/{choice}",
            start_time,
            end_time,
            targetname=f"assets/temp/{id}/background.mp4",
        )
    except (OSError, IOError):  # ffmpeg issue see #348
        print_substep("FFMPEG issue. Trying again...")
        with VideoFileClip(f"assets/backgrounds/{choice}") as video:
            new = video.subclip(start_time, end_time)
            new.write_videofile(f"assets/temp/{id}/background.mp4")

    print_substep("Background video chopped successfully!", style="bold green")
    return background_config[2]

def prepare_background(id: str, W: int, H: int) -> VideoFileClip:
    clip = (
        VideoFileClip(f"assets/temp/{id}/background.mp4")
            .without_audio()
            .resize(height=H)
    )

    # calculate the center of the background clip
    c = clip.w // 2

    # calculate the coordinates where to crop
    half_w = W // 2
    x1 = c - half_w
    x2 = c + half_w

    return clip.crop(x1=x1, y1=0, x2=x2, y2=H)

def prepare_video(id):
    bg_config = get_background_config()
    download_background(bg_config)
    _, audio_composite = make_audio(id)
    chop_background_video(bg_config, audio_composite.duration, id)
    background_clip = prepare_background(id, 1080, 1920)

    return background_clip, bg_config
