from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import pygame
from tkinter import filedialog
import os
import time
from mutagen.mp3 import MP3
from regex import *

def create_screen():
    global time_label, file_listbox, time_slider
    playlist_frame = ttk.LabelFrame(root, text="Playlist", style="Playlist.TLabelframe")
    playlist_frame.pack(pady=20, padx=10, fill="both", expand=True)
    file_listbox = Listbox(playlist_frame, bg="#F6F6F6", selectbackground="#C4E1FF", borderwidth=0, highlightthickness=0)
    file_listbox.pack(fill="both", expand=True)
    time_frame = ttk.Frame(root)
    time_frame.pack()
    time_label = ttk.Label(time_frame, text="00:00 / 00:00", style="Time.TLabel")
    time_label.grid(row=0, column=0)
    time_slider = ttk.Scale(time_frame, from_=0, to=100, value=0, length=300 ,command=slide)
    time_slider.grid(row=0, column=1, padx=10)
    control_frame = ttk.Frame(root)
    control_frame.pack(pady=20)
    add_button = ttk.Button(control_frame, text="Add Files", command= lambda: add_files(file_listbox), style="Add.TButton")
    add_button.grid(row=0, column=0, padx=10)
    play_button = ttk.Button(control_frame, text="Play", command= lambda: play_music(file_listbox), style="Play.TButton")
    play_button.grid(row=0, column=1, padx=10)   
    stop_button = ttk.Button(control_frame, text="Stop", command= stop_music, style="Stop.TButton")
    stop_button.grid(row=0, column=2, padx=10)

def slide(x):
    selected_file = file_listbox.get(ACTIVE)
    pygame.mixer.music.load(selected_file)
    pygame.mixer.music.play(start=int(time_slider.get()))

def song_length():
    if stopped:
        return
    global length
    current_time = int(pygame.mixer.music.get_pos() / 1000)
    new_time = time.strftime("%M:%S", time.gmtime(current_time))
    song = file_listbox.get(ACTIVE)
    song_mut = MP3(song)
    length = song_mut.info.length
    full_time = time.strftime("%M:%S", time.gmtime(length))
    new_time = time.strftime("%M:%S", time.gmtime(int(time_slider.get())))

    if int(time_slider.get()) == int(length):
        time_label.config(text=f"{full_time} / {full_time}")
    elif int(time_slider.get() + 1) == int(current_time):
        time_label.config(text=f"{new_time} / {full_time}")
        time_slider.config(to=int(length), value=int(current_time))
    else:
        time_label.config(text=f"{new_time} / {full_time}")
        next_time = int(time_slider.get()) + 1
        time_slider.config(to=int(length), value=next_time)

    time_label.after(1000, song_length)

def add_files(file_listbox):
    files = filedialog.askopenfilenames(filetypes = (("MP3 Files", "*.mp3"), ("All Files", "*.*")))
    for file in files:
        playlist.append(file)
        filename = os.path.basename(file)
        new_filename = sub(".mp3$", "", filename)
        file_listbox.insert(tk.END, new_filename)

def play_music(file_listbox):
    global stopped
    if pygame.mixer.music.get_busy():
        stopped = True
        pygame.mixer.music.stop()
    stopped = False
    selected_file = file_listbox.get(tk.ACTIVE)
    pygame.mixer.music.load(f"./{selected_file}")
    pygame.mixer.music.play()
    song_length()
    time_slider.config(to=int(length), value=0)

def stop_music():
    global stopped
    stopped = True
    time_slider.config(value=0)
    time_label.config(text="00:00 / 00:00")
    pygame.mixer.music.stop()

root = tk.Tk()
root.title("Music Player")
stopped = False

style = ttk.Style()
style.theme_use("clam")
style.configure("Playlist.TLabelframe", bg="#333333", fg="#FFFFFF", font=("Helvetica", 12, "bold"), relief="solid")
style.configure("Time.TLabel", fg="#333333", font=("Helvetica", 10))
style.map("Time.TLabel")
style.configure("Add.TButton", bg="#f8ca00", fg="#333333", font=("Helvetica", 12, "bold"), padding=10)
style.map("Add.TButton", bg=[("active", "#fedd55")])
style.configure("Play.TButton", bg="#00c853", fg="#333333", font=("Helvetica", 12, "bold"), padding=10)
style.map("Play.TButton", bg=[("active", "#4caf50")])
style.configure("Stop.TButton", bg="#e53935", fg="#333333", font=("Helvetica", 12, "bold"), padding=10)
style.map("Stop.TButton", bg=[("active", "#ff5252")])
playlist = []
pygame.init()
pygame.mixer.init()

create_screen()
root.mainloop()