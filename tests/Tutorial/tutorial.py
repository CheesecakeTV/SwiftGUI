import SwiftGUI as sg

sg.Themes.FourColors.Emerald()

layout = [
    *[
        [sg.In(highlightcolor="orange", highlightbackground_color="red")] for _ in range(30)
    ],[
        sg.In(),
    ],[
        sg.T("Test")
    ]
]

w = sg.Window([[sg.T("Hello world")]])
sw = sg.SubWindow(layout)
print(sw.root.winfo_width(), sw.root.winfo_height())
#sw.root.update_idletasks()
print(sw.root.winfo_width(), sw.root.winfo_height())

for e,v in w:
    ...


