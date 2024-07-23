import moviepy.editor as mpe
import random
import os

videvideo_extensions = []
def list_video_files(folder_path):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm']
    video_files = []

    for file_name in os.listdir(folder_path):
        if any(file_name.lower().endswith(ext) for ext in video_extensions):
            video_files.append(file_name)

    return video_files
video = list_video_files('Jshlatt')

def FinalRender(selectedOptions, callback=None):
    print(selectedOptions)
    # Define common resolution
    common_resolution = (1920, 1080)  # Change to desired resolution

    # Load all the video clips
    intro = mpe.VideoFileClip("intro.mp4")

    # Initialize the final video with the intro clip
    jshlattreact = intro

    # Concatenate clips randomly
    for i in range(len(selectedOptions)):
        reac = mpe.VideoFileClip(f"Result/output{i}.mp4")
        c = selectedOptions[i]
        if c == "Random":
            c = random.choice(video)
        reactionch = mpe.VideoFileClip(f"Jshlatt/{c}")
        
        clip = mpe.concatenate_videoclips([reac, reactionch])
        jshlattreact = mpe.concatenate_videoclips([jshlattreact, clip])

    # Resize final video while preserving aspect ratio
    jshlattreact = jshlattreact.resize(height=common_resolution[1])

    music_clip = mpe.AudioFileClip("music/music.mov")

    # Trim the music clip to match the duration of the video clip
    music_clip = music_clip.subclip(0, jshlattreact.duration)

    # Combine original video audio and music audio
    combined_audio = mpe.CompositeAudioClip([jshlattreact.audio, music_clip])

    # Overlay combined audio on video
    jshlattreact = jshlattreact.set_audio(combined_audio)

    # Write the final video
    jshlattreact.write_videofile("Result/jshlattreact.mp4", fps=30, remove_temp=True, codec="libx264", audio_codec="aac", threads=6)

    if callback:
            callback()
