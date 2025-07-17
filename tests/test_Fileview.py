from tkinter import filedialog as fd
import SwiftGUI as sg

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
    ]
]

w = sg.Window(layout)
w["MyButton"].push_once()
w["MyButton"].push_once()
w.close()

# for e,v in w:
#     print(e,v)

#print(fd.askopenfilename(filetypes=(("Image","png"),("JPEG","jpg")))) # Single file
#print(fd.askopenfilenames()) # Multiple files (name)

#print(fd.askopenfile()) # Opens the single file directly
#print(fd.askopenfiles())

#print(fd.askdirectory(title="Gib folder!"))
#print(fd.asksaveasfilename(defaultextension=".png",filetypes=(("IMG","jpeg"),)))

