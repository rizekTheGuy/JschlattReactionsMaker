import os
import moviepy.editor as mpe

def list_video_files(folder_path):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm']
    video_files = []

    for file_name in os.listdir(folder_path):
        if any(file_name.lower().endswith(ext) for ext in video_extensions):
            video_files.append(file_name)

    return video_files

memes = list_video_files("Videos")
music = mpe.AudioFileClip("music/2AM.mp3")

def ShortsMaker(ISMusic, callback=None):
    for meme in memes:
        video = mpe.VideoFileClip(f"Videos/{meme}")
        idle = mpe.VideoFileClip("Idle.mp4")

        if ISMusic:
            background_music = music.subclip(0, video.duration)
            mixed_audio = mpe.CompositeAudioClip([video.audio, background_music.volumex(0.2)]) # Adjust volume of the background music

            # Set the mixed audio to the video
            video = video.set_audio(mixed_audio)

        # Step 1: Scale the video to fit 1080 px width
        if video.w < video.h:
            video_scaled = video.resize(width=1080)
        else :
            video_scaled = video.resize(width=1080, height=1150)

        # Step 2: Crop the video to fit the bottom 1150 px of a 1920 px canvas
        height = video_scaled.h
        crop_y1 = (height - 1150)/2 # Starting y position for cropping
        crop_y2 = height-((height - 1150)/2)  # Ending y position for cropping

        video_cropped = video_scaled.crop(y1=crop_y1, y2=crop_y2)

        idle_duration = idle.duration
        video_duration = video_cropped.duration

        # Step 3: Trim the idle video to match the duration of the meme video
        idle_trimmed = idle.subclip(idle_duration-video_duration, idle_duration)

        # Step 4: Position the cropped meme video on top of the idle video
        video_positioned = video_cropped.set_position(("center", "bottom"))

        # Create a CompositeVideoClip with the idle video as the background
        final_video = mpe.CompositeVideoClip([idle_trimmed, video_positioned])

        # Save the resulting video
        final_video.write_videofile(f"Result/{meme}output.mp4", codec='libx264')
    if callback:
        callback()