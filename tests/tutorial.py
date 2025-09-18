import SwiftGUI as sg
import threading
import time

### Global options ###
sg.Themes.FourColors.Jungle()
# sg.Examples.preview_all_elements()
# exit()

### Layout ###
my_frame = sg.Frame([
    [
        grid := sg.GridFrame([
            [tex := sg.T("Hi", width=30), sg.VSep(), sg.T("World")],
            [sg.HSep() for i in range(4)],
            [
                sg.T("World",expand_y=True, background_color="red", expand=False),
                sg.VSep(),
                sg.T("Hi"),
                sg.Listbox(range(15), key="LB", default_event=True, key_function= lambda w,e,val,v:print("EV:",e,val,w[e],v))
            ],
            [
                sg.Table(),
                sg.Combo(("Hi", "World"))
            ]
        ], alignment= "right")
    ]
])

baseHandler = sg.BaseKeyHandler()

layout = [
    [
        sg.Input("Hallo Welt", key="In", default_event= True),
    ]
]

w = sg.Window(layout, grab_anywhere=True)
baseHandler._init(my_frame, w.root, grab_anywhere_window=w)

### Additional configurations/actions ###

### Main loop ###
for e,v in w:
    print(e, v)


### After window was closed ###
