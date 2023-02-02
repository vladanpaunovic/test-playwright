from os.path import exists
from os import makedirs
from typing import Final
from utils.cleanup import cleanup
from utils.video import Video
from utils.console import print_step, print_substep
from moviepy.audio.io.AudioFileClip import AudioFileClip
from rich.progress import track
from moviepy.audio.AudioClip import concatenate_audioclips, CompositeAudioClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.audio.fx.volumex import volumex
from moviepy.video.tools.subtitles import SubtitlesClip, TextClip
from moviepy.editor import *

import multiprocessing
import json

# settings values
W: Final[int] = 1080
H: Final[int] = 1920
transition = 0.2
opacity = 0.9

def make_audio(id):
    files = [f for f in os.listdir(f"assets/temp/{id}/audio") if f.endswith(".wav")]
    length = len(files)

    print_step("Making the audio... 🎧")

    audio_clips = [
        AudioFileClip(f"assets/temp/{id}/audio/audio-{i + 1}.wav")
        for i in track(
            range(0, length), "Collecting the audio files..."
        )
    ]

    audio_concat = concatenate_audioclips(audio_clips)
    audio_composite = CompositeAudioClip([audio_concat])

    return audio_clips, audio_composite

def assemble_screenshots(id, audio_clips, background_config):
    number_of_clips = len(audio_clips) - 1

    print_step("Making the final video... 🎬")

    image_clips = []
    new_opacity = 1 if opacity is None or float(opacity) >= 1 else float(opacity)

    screenshot_width = int((W * 90) // 100)

    subs = []
    for i, audio_clip in enumerate(audio_clips):
        if i == 0:
            subs.append((0, audio_clip.end))
        else:
            start = subs[i - 1][1]
            end = start + audio_clip.end
            subs.append((start, end))

    # Gather all images
    for i in track(
        range(0, number_of_clips), "Collecting the image files..."
    ):
        print("Collecting the image files...", i)

        image_clips.append(
            ImageClip(f"assets/temp/{id}/png/screenshot-{i + 1}.png")
                .set_start(subs[i][0])
                .set_end(subs[i][1])
                .resize(width=screenshot_width)
                .set_opacity(new_opacity)
        )

    img_clip_pos = background_config[3]

    image_concat = concatenate_videoclips(image_clips).set_position(img_clip_pos)  # note transition kwarg for delay in imgs

    return image_concat

def assemble_subtitles(id, audio_clips):
    subtitles_width = int((W * 80) // 100)
    subtitles_hight = 280

    # Subtitles
    generator = lambda txt: TextClip(txt, font='Avenir-Next-Demi-Bold', fontsize=70, color='white', stroke_color="black", stroke_width=3, align="center", method="caption", size=(subtitles_width, subtitles_hight))

    with open(f"assets/temp/{id}/audio/messages.json") as infile:
        messages = json.load(infile)

    subs = []

    for i, audio_clip in enumerate(audio_clips):
        if i == 0:
            subs.append(((0, audio_clip.end), messages[i]))
        else:
            start = subs[i - 1][0][1]
            end = start + audio_clip.end
            subs.append(((start, end), messages[i]))

    subtitles_h_position = H - (subtitles_hight + 150)
    subtitles = SubtitlesClip(subs, generator).set_position(("center", subtitles_h_position)).set_opacity(opacity)

    return subtitles


def make_final_video(background_clip, id, background_config):
    audio_clips, audio_composite = make_audio(id)
    image_concat = assemble_screenshots(id, audio_clips, background_config)
    image_concat.audio = audio_composite

    # Subtitles
    subtitles = assemble_subtitles(id, audio_clips)

    final = CompositeVideoClip([background_clip, image_concat, subtitles])

    if not exists(f"./results/{id}"):
        print_substep("The results folder didn't exist so I made it")
        makedirs(f"./results/{id}")

    final.write_videofile(
        f"assets/temp/{id}/temp.mp4",
        fps=30,
        audio_codec="aac",
        audio_bitrate="192k",
        verbose=False,
        remove_temp=True,
        threads=multiprocessing.cpu_count(),
        preset="ultrafast", # for testing purposes
    )

    ffmpeg_extract_subclip(
        f"assets/temp/{id}/temp.mp4",
        0,
        audio_composite.duration,
        targetname=f"results/{id}/final-video.mp4",
    )

    print_step("Removing temporary files 🗑")
    cleanups = cleanup(id)
    print_substep(f"Removed {cleanups} temporary files 🗑")
    print_substep("See result in the results folder!")