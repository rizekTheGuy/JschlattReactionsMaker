import customtkinter
from PIL import Image
import pygame
import os
import threading
import moviepy.editor as mpe
import random
import jshlattputtogether
import YTShorts

# Initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.load("assets/Music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

optionmenus = []
selected_options = []

# Function to play music
def Play():
    pygame.mixer.music.play(-1)

# Function to stop music
def Stop():
    pygame.mixer.music.stop()

# Function to get the selected options
def get_selected_options():
    selected_options = [optionmenu.get() for optionmenu in optionmenus]
    print("Selected options:", selected_options)
    return selected_options

# Function to list video files in a folder
def list_video_files(folder_path):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.webm']
    video_files = []

    for file_name in os.listdir(folder_path):
        if any(file_name.lower().endswith(ext) for ext in video_extensions):
            video_files.append(file_name)

    return video_files

# Function to render videos
def Render1(selected_options):
    global status_label

    videosAll = list_video_files('Videos')

    looking1 = mpe.VideoFileClip("Jshlatt/Looking/looking1.mp4")
    looking2 = mpe.VideoFileClip("Jshlatt/Looking/looking2.mp4")
    looking3 = mpe.VideoFileClip("Jshlatt/Looking/looking3.mp4")
    looking4 = mpe.VideoFileClip("Jshlatt/Looking/looking4.mp4")

    looking = [looking1, looking2, looking3, looking4]

    blackimg = mpe.ImageClip("blackcanvas.png")
    k = 0
    total_videos = len(videosAll)

    for idx, i in enumerate(videosAll):
        # Update status label
        update_status(f"Rendering video {idx + 1} of {total_videos}...")

        # Choose a random looking clip
        lookch = random.choice(looking)

        # Load the meme video clip
        meme_clip = mpe.VideoFileClip(f"Videos/{i}")

        scale_factor = min(blackimg.w / meme_clip.w, blackimg.h / meme_clip.h)

        # Resize the clip while maintaining aspect ratio
        meme_clip = meme_clip.resize(width=int(meme_clip.w * scale_factor))

        meme_clip = mpe.CompositeVideoClip([blackimg.set_duration(meme_clip.duration), meme_clip.set_position('center')])

        # Define crop coordinates
        x1, y1 = 350, 20  # Top-left corner
        x2, y2 = 1450, 1060  # Bottom-right corner

        # Manipulate the looking clip to match the duration of the meme
        memeduration = meme_clip.duration
        lookd = lookch.duration
        while lookd < memeduration:
            lookch = mpe.concatenate_videoclips([lookch, lookch])
            lookd = lookch.duration
        lookch = lookch.subclip(0, memeduration)

        # Crop the looking clip
        cropped_clip = lookch.crop(x1=x1, y1=y1, x2=x2, y2=y2)

        # Resize the looking clip
        new_width = cropped_clip.w // 3
        new_height = cropped_clip.h // 3
        look = cropped_clip.resize((new_width, new_height))

        # Composite the meme and the looking clip
        final_video = mpe.CompositeVideoClip([meme_clip, look])

        # Write the final clip to a file
        output_path = f"Result/output{k}.mp4"
        k += 1
        final_video.write_videofile(output_path, fps=30, remove_temp=True, codec="libx264", audio_codec="aac", threads=6)

    # Update status label after rendering is complete
    update_status("Putting Stuff Together...")
    #jshlattputtogether.FinalRender(selected_options)
    JPT_thread = threading.Thread(target=jshlattputtogether.FinalRender, args=(selected_options, on_JPT_done))
    JPT_thread.start()

def on_JPT_done():
    update_status("Rendering Complete!")

# Function to update the status label (thread-safe)
def update_status(message):
    def callback():
        status_label.configure(text=message)
    app.after(0, callback)

# Function to run Render1 in a separate thread
def render_videos_threaded():
    if selectedOP.get() == "Youtube Video":
        selected_options = get_selected_options()
        update_status("Rendering in Progress...")

        # Start a separate thread for the video rendering process
        render_thread = threading.Thread(target=Render1, args=(selected_options,))
        render_thread.start()
    else:
        def on_shorts_done():
            update_status("Rendering Complete!")
        
        # Start a separate thread for the ShortsMaker process
        update_status("Rendering in Progress...")
        shorts_thread = threading.Thread(target=YTShorts.ShortsMaker, args=(checkbox.get(), on_shorts_done))
        shorts_thread.start()

def optionmenu_callback(choice):
    if choice == "Youtube Shorts":
        checkbox.configure(state="normal")
        optionmenuReactions.configure(state="disabled")
    else:
        checkbox.configure(state="disabled")
        optionmenuReactions.configure(state="normal")

# Get the list of video files
videos = list_video_files('Videos')
reactions = list_video_files('Jshlatt')

# Create the main window
app = customtkinter.CTk()
image = Image.open("assets/Background.png")
background_image = customtkinter.CTkImage(image, size=(800, 800))
app.geometry("800x800")
app.maxsize(800, 800)
app.minsize(700, 0)
app.title("Jschlatt")
app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=50)
selectedOP = customtkinter.StringVar(value="Youtube Video")

def bg_resizer(e):
    if e.widget is app:
        i = customtkinter.CTkImage(image, size=(e.width, e.height))
        bg_lbl.configure(text="", image=i)

# Create a background label
bg_lbl = customtkinter.CTkLabel(app, text="", image=background_image)
bg_lbl.place(x=0, y=0)

# Create the main title
Text = customtkinter.CTkLabel(app, text="Jschlatt reaction videos Maker", fg_color="transparent", font=("arial", 35))
Text.grid(padx=(175, 0), pady=15)

# Create a label for the video type
Text = customtkinter.CTkLabel(app, text="Video Type : ", fg_color="transparent", font=("arial", 10))
Text.grid(row=1, column=0, padx=(150, 0), pady=10, sticky=customtkinter.W)

# Create an option menu for video types
optionmenu = customtkinter.CTkOptionMenu(app, values=["Youtube Video", "Youtube Shorts"], command=optionmenu_callback, variable=selectedOP)
optionmenu.set("Youtube Video")
optionmenu.grid(row=1, column=0, padx=(0, 10), pady=10)

checkbox = customtkinter.CTkCheckBox(app, text="Shorts With Music")
checkbox.grid(row=1, column=1, padx=(0, 0), pady=10, sticky=customtkinter.W)
checkbox.configure(state="disabled")

# Create labels and option menus for each video
j = 2
for i in videos:
    Text = customtkinter.CTkLabel(app, text=i, fg_color="transparent", font=("arial", 10))
    Text.grid(row=j, column=0, padx=(25, 0), pady=10, sticky=customtkinter.W)

    optionmenuReactions = customtkinter.CTkOptionMenu(app, values=reactions)
    optionmenuReactions.set("Random")
    optionmenuReactions.grid(row=j, column=1, padx=(0, 10), pady=10)

    optionmenus.append(optionmenuReactions)  # Append each option menu to the list

    j += 1

# Create a button to render the selected options
button = customtkinter.CTkButton(app, text="Render", command=render_videos_threaded)
button.grid(row=50, column=0, padx=(175, 0), pady=35)

# Create buttons to control music playback
button = customtkinter.CTkButton(app, text="Play Music", command=Play)
button.grid(row=51, column=0, padx=(0, 430), pady=0)

button = customtkinter.CTkButton(app, text="Stop Music", command=Stop)
button.grid(row=51, column=1, padx=(0, 0), pady=0)

# Add a status label to indicate rendering progress
status_label = customtkinter.CTkLabel(app, text="Press Render to Start Rendering")
status_label.grid(row=52, column=0, padx=(175, 0), pady=10)

# Set the window icon
app.iconbitmap("./Jschlat.ico")

# Start the main event loop
app.mainloop()
