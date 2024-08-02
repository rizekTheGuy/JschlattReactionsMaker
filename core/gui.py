import customtkinter
import pygame
import threading
import moviepy.editor as mpe
import random
from core.render import render_video, render_short
from core.utils import list_video_files
from PIL import Image


class Gui:
    def __init__(self) -> None:
        self.option_menus = []
        self.selected_options = []
        
        self.app = customtkinter.CTk()
        self.status_label = None
        self.checkbox = None 
        self.optionmenuReactions = None
        self.selectedOP = None
        
        pygame.mixer.init()
        pygame.mixer.music.load("assets/Music.mp3")
        pygame.mixer.music.set_volume(0.3)
    
    def __call__(self) -> None:
        videos = list_video_files('Videos')
        reactions = list_video_files('Jshlatt')
        
        image = Image.open("assets/Background.png")
        background_image = customtkinter.CTkImage(image, size=(800, 800))
        self.app.geometry("800x800")
        self.app.maxsize(800, 800)
        self.app.minsize(700, 400)
        self.app.title("Jschlatt")
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=50)
        self.selectedOP = customtkinter.StringVar(value="Youtube Video")

        bg_lbl = customtkinter.CTkLabel(self.app, text="", image=background_image)
        bg_lbl.place(x=0, y=0)

        Text = customtkinter.CTkLabel(self.app, text="Jschlatt reaction videos Maker", fg_color="transparent", font=("arial", 35))
        Text.grid(padx=(175, 0), pady=15)

        Text = customtkinter.CTkLabel(self.app, text="Video Type : ", fg_color="transparent", font=("arial", 10))
        Text.grid(row=1, column=0, padx=(150, 0), pady=10, sticky=customtkinter.W)

        optionmenu = customtkinter.CTkOptionMenu(self.app, values=["Youtube Video", "Youtube Shorts"], command=self.optionmenu_callback, variable=self.selectedOP)
        optionmenu.set("Youtube Video")
        optionmenu.grid(row=1, column=0, padx=(0, 10), pady=10)

        self.checkbox = customtkinter.CTkCheckBox(self.app, text="Shorts With Music")
        self.checkbox.grid(row=1, column=1, padx=(0, 0), pady=10, sticky=customtkinter.W)
        self.checkbox.configure(state="disabled")

        j = 2 #TODO
        for video in videos:
            Text = customtkinter.CTkLabel(self.app, text=video, fg_color="transparent", font=("arial", 10))
            Text.grid(row=j, column=0, padx=(25, 0), pady=10, sticky=customtkinter.W)

            self.optionmenuReactions = customtkinter.CTkOptionMenu(self.app, values=reactions)
            self.optionmenuReactions.set("Random")
            self.optionmenuReactions.grid(row=j, column=1, padx=(0, 10), pady=10)

            self.option_menus.append(self.optionmenuReactions)

            j += 1

        button = customtkinter.CTkButton(self.app, text="Render", command=self.render_videos_threaded)
        button.grid(row=50, column=0, padx=(175, 0), pady=35)

        button = customtkinter.CTkButton(self.app, text="Play Music", command=lambda : pygame.mixer.music.play(-1))
        button.grid(row=51, column=0, padx=(0, 430), pady=0)

        button = customtkinter.CTkButton(self.app, text="Stop Music", command=lambda: pygame.mixer.music.stop())
        button.grid(row=51, column=1, padx=(0, 0), pady=0)

        self.status_label = customtkinter.CTkLabel(self.app, text="Press Render to Start Rendering")
        self.status_label.grid(row=52, column=0, padx=(175, 0), pady=10)

        self.app.iconbitmap("./Jschlat.ico")

        self.app.mainloop()

    def get_selected_options(self):
        selected_options = [option_menu.get() for option_menu in self.option_menus]
        print("Selected options:", selected_options)
        return selected_options

    def render_video(self, selected_options):

        videosAll = list_video_files('Videos')

        looking1 = mpe.VideoFileClip("Jshlatt/Looking/looking1.mp4")
        looking2 = mpe.VideoFileClip("Jshlatt/Looking/looking2.mp4")
        looking3 = mpe.VideoFileClip("Jshlatt/Looking/looking3.mp4")
        looking4 = mpe.VideoFileClip("Jshlatt/Looking/looking4.mp4")

        looking = [looking1, looking2, looking3, looking4]

        blackimg = mpe.ImageClip("./assets/blackcanvas.png")
        k = 0
        total_videos = len(videosAll)

        for idx, i in enumerate(videosAll):
            self.update_status(f"Rendering video {idx + 1} of {total_videos}...")

            lookch = random.choice(looking)

            meme_clip = mpe.VideoFileClip(f"Videos/{i}")

            scale_factor = min(blackimg.w / meme_clip.w, blackimg.h / meme_clip.h)

            meme_clip = meme_clip.resize(width=int(meme_clip.w * scale_factor))

            meme_clip = mpe.CompositeVideoClip([blackimg.set_duration(meme_clip.duration), meme_clip.set_position('center')])

            x1, y1 = 350, 20  # Top-left corner
            x2, y2 = 1450, 1060  # Bottom-right corner

            memeduration = meme_clip.duration
            lookd = lookch.duration
            while lookd < memeduration:
                lookch = mpe.concatenate_videoclips([lookch, lookch])
                lookd = lookch.duration
            lookch = lookch.subclip(0, memeduration)

            cropped_clip = lookch.crop(x1=x1, y1=y1, x2=x2, y2=y2)

            new_width = cropped_clip.w // 3
            new_height = cropped_clip.h // 3
            look = cropped_clip.resize((new_width, new_height))

            final_video = mpe.CompositeVideoClip([meme_clip, look])

            output_path = f"Result/output{k}_{''.join(k for k in random.choices("abcdefghijklmnpqrstuvwxyz", k=8))}.mp4"
            k += 1
            final_video.write_videofile(output_path, fps=30, remove_temp=True, codec="libx264", audio_codec="aac", threads=6)

        self.update_status("Putting Stuff Together...")
        
        threading.Thread(target=render_video, args=(selected_options, lambda: self.update_status("Rendering Complete!"))).start()

    def update_status(self, message):
        self.app.after(0, lambda: self.status_label.configure(text=message))

    def render_videos_threaded(self):
        if self.selectedOP.get() == "Youtube Video":
            selected_options = self.get_selected_options()
            self.update_status("Rendering in Progress...")

            render_thread = threading.Thread(target=self.render_video, args=(selected_options,))
            render_thread.start()
        else:
            def on_shorts_done():
                self.update_status("Rendering Complete!")

            self.update_status("Rendering in Progress...")
            shorts_thread = threading.Thread(target=render_short, args=(self.checkbox.get(), on_shorts_done))
            shorts_thread.start()

    def optionmenu_callback(self, choice):
        if choice == "Youtube Shorts":
            self.checkbox.configure(state="normal")
            self.optionmenuReactions.configure(state="disabled")
        else:
            self.checkbox.configure(state="disabled")
            self.optionmenuReactions.configure(state="normal")

