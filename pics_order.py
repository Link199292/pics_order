from PIL import Image
import os
from tkinter import Tk
from tkinter import filedialog

def photo_order():

    #I/O folders----------------------------------------------------------------
    print("Select your input folder")
    root = Tk()
    root.withdraw()
    from_path = filedialog.askdirectory()
    print(from_path)
    print("Select your output folder")
    from_path = from_path.replace("/", "\\")
    to_path = filedialog.askdirectory()
    to_path = to_path.replace("/", "\\")
    print("You have selected:\nInput:   {}\nOutput:   {}".format(from_path,
    to_path))
    print("Let's start!")
    os.system("pause")

    #Change path----------------------------------------------------------------
    os.chdir(from_path)

    #Init months list for number - month name conversion------------------------
    month = ["", "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
    "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

    #list of extensions---------------------------------------------------------
    lst = [".jpg", ".jpeg", ".cr2", ".arw"]

    #Init instructions list for file move---------------------------------------
    instructions = []

    #Init counter for file which has been moved and files which have been not---
    goodcount = 0
    badcount = 0

    for root, dirs, files in os.walk(from_path):
        for file in files:
            if file.lower().endswith((tuple(lst))):
                try:
                    with (Image.open(file)) as img:
                        img = Image.open(file)
                        exif = img.getexif()
                        creation_time = exif.get(36867).split(" ")
                        date = creation_time[0]
                        y, m, d = date.split(":")
                        print("# {:<15s}      Data: {}-{}-{}".format(file, d, m, y))
                        goodcount += 1
                except:
                    print("# {:<15s}      No info sulla data!".format(file))
                    badcount += 1
                    continue
                m = month[int(m)]
                if y not in os.listdir(to_path):
                    os.mkdir(os.path.join(to_path, y))
                if m not in os.listdir(os.path.join(to_path, y)):
                    os.mkdir(os.path.join(to_path, y, m))
                if d not in os.listdir(os.path.join(to_path, y, m)):
                    os.mkdir(os.path.join(to_path, y, m, d))
                instructions.append(f"copy \"{os.path.join(from_path,file)}\" \"{os.path.join(to_path, y, m, d)}\"")

    #Execute instructions-----------------------------------------------------
    for i in instructions:
        os.system(i)
    print("Found files: {} \nMoved files: {}".format(goodcount +
    badcount, goodcount))

photo_order()
os.system("pause")
