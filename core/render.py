import moviepy.editor as mpe
import random
from core.utils import list_video_files

video = list_video_files('Jshlatt')

def render_video(selectedOptions, callback=None):
    common_resolution = (1920, 1080)  

    intro = mpe.VideoFileClip("./assets/intro.mp4")

    jshlattreact = intro

    for i in range(len(selectedOptions)):
        reac = mpe.VideoFileClip(f"Result/output{i}.mp4")
        c = selectedOptions[i]
        if c == "Random":
            c = random.choice(video)
        reactionch = mpe.VideoFileClip(f"Jshlatt/{c}")
        
        clip = mpe.concatenate_videoclips([reac, reactionch])
        jshlattreact = mpe.concatenate_videoclips([jshlattreact, clip])

    jshlattreact = jshlattreact.resize(height=common_resolution[1])

    music_clip = mpe.AudioFileClip("music/Tax Office (Day).mp3")

    music_clip = music_clip.subclip(0, jshlattreact.duration)

    combined_audio = mpe.CompositeAudioClip([jshlattreact.audio, music_clip])

    jshlattreact = jshlattreact.set_audio(combined_audio)

    jshlattreact.write_videofile("Result/jshlattreact.mp4", fps=30, remove_temp=True, codec="libx264", audio_codec="aac", threads=6)

    if callback:
            callback()

def render_short(ISMusic, callback=None):
    music = mpe.AudioFileClip("music/2AM.mp3")
    for meme in list_video_files("Videos"):
        video = mpe.VideoFileClip(f"Videos/{meme}")
        idle = mpe.VideoFileClip("./assets/Idle.mp4")

        if ISMusic:
            background_music = music.subclip(0, video.duration)
            mixed_audio = mpe.CompositeAudioClip([video.audio, background_music.volumex(0.2)]) 

            video = video.set_audio(mixed_audio)

        if video.w < video.h:
            video_scaled = video.resize(width=1080)
        else :
            video_scaled = video.resize(width=1080, height=1150)

        height = video_scaled.h
        crop_y1 = (height - 1150)/2 # Starting y position for cropping
        crop_y2 = height-((height - 1150)/2)  # Ending y position for cropping

        video_cropped = video_scaled.crop(y1=crop_y1, y2=crop_y2)

        idle_duration = idle.duration
        video_duration = video_cropped.duration

        idle_trimmed = idle.subclip(idle_duration-video_duration, idle_duration)

        video_positioned = video_cropped.set_position(("center", "bottom"))

        final_video = mpe.CompositeVideoClip([idle_trimmed, video_positioned])

        final_video.write_videofile(f"Result/{meme}output.mp4", codec='libx264')
    if callback:
        callback()