import SwiftGUI as sg

### Global options ###


### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.T(
            # \n is the newline-character and will add a line-break
            "I'm a text.\nI have a couple of options you should know about...",
            width=60,   # Reserve space for 30 characters long, no matter how long the text actually is
            background_color=sg.Color.gold,    # Background-color
            text_color=sg.Color.navy,  # Text/font-color

            fonttype=sg.font_windows.Comic_Sans_MS, # Who doesn't like comic-sans?
            fontsize=14,    # Size of the text
        )
    ]
]

w = sg.Window(layout)

### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    ...

### After window was closed ###
