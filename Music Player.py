from tkinter import *
from tkinter import filedialog
import pygame
import os

root = Tk()
root.title('Music Player')
root.geometry('1920x1080')
root.directory = ""  # will be set after folder selection

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = False


def load_music():
    global current_song, songs
    songs.clear()
    songlist.delete(0, END)
    # Let user pick a directory
    root.directory = filedialog.askdirectory()

    if not root.directory:
        return  # user cancelled folder selection

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext.lower() == '.mp3':
            songs.append(song)  # full filename with extension
            songlist.insert(END, name)  # display name without extension

    if songs:
        songlist.selection_set(0)
        current_song = songs[0]
        print("Songs loaded:", songs)
        print("Current song:", current_song)


def play_music():
    global current_song, paused
    if not current_song:
        print("No song selected.")
        return

    try:
        full_path = os.path.join(root.directory, current_song)
        print("Playing:", full_path)

        if not paused:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.unpause()
            paused = False
    except pygame.error as e:
        print("Error playing music:", e)


def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True


def next_music():
    global current_song, paused
    try:
        current_index = songs.index(current_song)
        next_index = current_index + 1
        if next_index < len(songs):
            songlist.selection_clear(0, END)
            songlist.selection_set(next_index)
            current_song = songs[next_index]
            play_music()
        else:
            print("Already at last song.")
    except Exception as e:
        print("Error in next_music:", e)


def prev_music():
    global current_song, paused
    try:
        current_index = songs.index(current_song)
        prev_index = current_index - 1
        if prev_index >= 0:
            songlist.selection_clear(0, END)
            songlist.selection_set(prev_index)
            current_song = songs[prev_index]
            play_music()
        else:
            print("Already at first song.")
    except Exception as e:
        print("Error in prev_music:", e)


organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label="Select Folder", command=load_music)
menubar.add_cascade(label="Organise", menu=organise_menu)

songlist = Listbox(root, bg="black", fg="white", width=100, height=30)
songlist.pack()

play_btn_img = PhotoImage(file="but/play.png")
pause_btn_img = PhotoImage(file="but/pause.png")
next_btn_img = PhotoImage(file="but/next.png")
prev_btn_img = PhotoImage(file="but/prev.png")

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_img, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_img, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_img, borderwidth=0, command=prev_music)

play_btn.grid(row=0, column=1, padx=10, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

root.mainloop()
