from PIL import ImageTk
from PIL import Image
import SwiftGUI as sg
import tkinter as tk
from pathlib import Path
import base64
import io

# img = Image.open("Pixelkatze.png").tobytes()
# img = base64.b32encode(img)
# img = Image.frombytes(base64.b32decode(img))
img = sg.file_to_b64("Pixelkatze.png")
print(img)
img = sg.file_from_b64(img)

layout = [
    [
        text := sg.T("Das ist ein Test")
    ],[
        button := sg.Button("Test")
    ],[
        image := sg.Image(img).bind_event(sg.Event.ClickLeft, key= "Img_Click")
    ]
]

img = Image.open("Anime.jpg")
w = sg.Window(layout, icon=img)
#w.update(icon = "Anja.ico")
#w.root.iconphoto("Pixelkatze.")

#w.root.configure(icon = image)

for e,v in w:
    print(e,v)
    image.update(height = 150)



