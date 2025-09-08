import SwiftGUI as sg
import threading
import time

### Global options ###
sg.Themes.FourColors.Emerald()
sg.Examples.preview_all_elements()
exit()

### Layout ###
layout = [
    [
        my_text := sg.T("Some text", fontsize= 24), # Don't leave the layout empty
    ],[
        my_progress := sg.Progressbar(9, expand= True, number_max= 100),
    ],[
        sg.ProgressbarVertical(30)
    ]
]

w = sg.Window(layout)

### Additional configurations/actions ###

### Main loop ###
for e,v in w:
    print(e, v)


### After window was closed ###
