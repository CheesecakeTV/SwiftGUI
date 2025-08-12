import SwiftGUI as sg

"""
This example shows how to use the event-loop.

Refer to 
https://github.com/CheesecakeTV/SwiftGUI/blob/main/Docs/01%20Basic%20tutorials/01%20Getting-started.md#breaking-out-of-the-loop-events
for more information.
"""

### Global options ###


### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.Button(
            "Button 1",
            key="B1",
            fontsize=14,
        ),
        sg.Button(
            "Button 2",
            key="B2",
            fontsize=14,
        )
    ],[
        sg.In(
            fontsize=20,
            default_event=True,
            key="Input"
        )
    ]
]

w = sg.Window(layout)

### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    print("Event:",e)

    if e == "Input":
        print("The sg.Input was changed!")

    if e == "B1":
        print("Button 1 was pressed!")

    if e == "B2":
        print("Button 2 was pressed!")

### After window was closed ###
