import SwiftGUI as sg
import threading
import time

### Global options ###
sg.Themes.FourColors.Emerald()
# sg.GlobalOptions.Separator.padding = 0
# sg.Examples.preview_all_elements()
# exit()

### Layout ###
layout = [
    [
        grid := sg.GridFrame([
            [tex := sg.T("Hi", width=30), sg.VSep(), sg.T("World")],
            [sg.HSep() for i in range(4)],
            [sg.T("World",expand_y=True, background_color="red", expand=False), sg.VSep(), sg.T("Hi"), sg.Listbox(range(15))],
        ], alignment= "right")
    ]
]

w = sg.Window(layout)

### Additional configurations/actions ###

### Main loop ###
for e,v in w:
    print(e, v)


### After window was closed ###
