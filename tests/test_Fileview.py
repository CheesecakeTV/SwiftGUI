from tkinter import filedialog as fd
import SwiftGUI as sg
from SwiftGUI import Color

layout = [
    [
        sg.FileBrowseButton(
            "Test",
            fontsize=24,
            key="MyButton",
            key_function=lambda val:print(repr(val)),
            file_browse_filetypes=(("All files","*"),),
            file_browse_initial_dir=".",
            file_browse_initial_file="vcs.xml",
            #file_browse_type="save_single",
        )
    ],[
        sg.ColorChooserButton(
            "Choose Color",
            key="Color",
            fontsize=24,
            initial_color=Color.SeaGreen1,
            key_function=lambda val:w.update(background_color = val)
        )
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

