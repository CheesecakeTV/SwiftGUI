import SwiftGUI as sg

### Global options ###


### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.ImageButton(
            "python-logo.png",
            key= "ImageClicked",
            width= 100,
        ),
    ]
]

w = sg.Window(layout, icon="python-logo-small.jpeg")

### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    ...

### After window was closed ###
