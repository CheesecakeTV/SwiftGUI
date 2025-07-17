from tkinter import filedialog as fd
import SwiftGUI as sg



layout = [
    [
        sg.FileBrowseButton("Test",fontsize=24,key="MyButton",key_function=lambda val:print(val))
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e,v)

#print(fd.askopenfilename(filetypes=(("Image","png"),("JPEG","jpg")))) # Single file
#print(fd.askopenfilenames()) # Multiple files (name)

#print(fd.askopenfile()) # Opens the single file directly
#print(fd.askopenfiles())

#print(fd.askdirectory(title="Gib folder!"))
#print(fd.asksaveasfilename(defaultextension=".png",filetypes=(("IMG","jpeg"),)))

