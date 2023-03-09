import threading
import time
from tkinter import *
import ctypes
import subprocess
import os
import platform
import secrets
from tkinter import filedialog
import tkinter.messagebox as tkm
import audioread
secretsGenerator = secrets.SystemRandom()
user32 = ctypes.windll.user32
screensize = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
root = Tk()
width_screen = int(int(screensize[0])//2)
height_screen = int(int(screensize[1])//2)
root.geometry(f"{width_screen}x{height_screen}")
root.title("True Shuffler")
root.update()
# Heading
title = Label(root, text="True Shuffler ~ HauseMaster", font=("Aerial", 13))
title.grid(row=0, column=1)

Directory = ""
dir_musics = []


def playAction():
    global dir_musics
    global Directory
    if Directory == "":
        tkm.showinfo("Please Provide Music Directory")
        return
    secure_choice = secretsGenerator.choice(dir_musics)
    tmp = ""
    tmp += Directory + "//" + secure_choice
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', tmp))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(tmp)
    else:                                   # linux variants
        subprocess.call(('xdg-open', tmp))
    with audioread.audio_open(tmp) as f:
        totalsec = f.duration
        time.sleep(float(totalsec))
        playAction()


audio_set = set(["m4a", "mp3", "aac", "webm", "flv"])


def openFilePicker():
    global dir_musics
    global Directory
    global directory_box
    Directory = filedialog.askdirectory()
    Directory += "/"
    directory_box.delete("1.0", END)
    directory_box.insert("1.0", Directory)
    Directory.replace("/", "//")
    tmp = os.listdir(Directory)
    dir_list = []
    for i in tmp:
        if i.split(".")[-1] in audio_set:
            dir_list.append(i)
    dir_musics = dir_list[::]

def updateHeight(event):
    global directory_box
    directory_box.config(height=directory_box.get('1.0', END).count('\n'))


Select = Button(root, text="Select Music Folder", command=openFilePicker)
Select.place(relx=0.01, rely=0.5, anchor=W)

directory_box = Text(root, fg="black", highlightthickness="1",
                     height=1, bg="yellow")
directory_box.place(relwidth=0.7, relx=0.5, rely=0.5, anchor=CENTER)
directory_box.bind("<Key>", updateHeight)
Directory.replace("/", "//")

myDown = Button(root, text="True Shuffle!", command=threading.Thread(
    target=playAction).start, padx=6, pady=10)
myDown.place(relx=0.99, rely=0.5, anchor=E)

root.mainloop()
