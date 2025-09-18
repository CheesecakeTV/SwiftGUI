from typing import Any

import SwiftGUI as sg
import threading
import time

from SwiftGUI.Windows import ValueDict

### Global options ###
sg.Themes.FourColors.SinCity()
# sg.Examples.preview_all_elements()
# exit()

class ButtonMat(sg.BaseCombinedElement):
    def __init__(self):
        frame = sg.GridFrame([[
            sg.Button(str(i), width= 3, key= str(i)) for i in range(15)
        ]])

        super().__init__(frame, "Hi")

    def _event_loop(self, e: Any, v: ValueDict):
        print("Combined loop:\t", e, v)
        v[e] = "C"
        self.w[e].update(background_color = "#" + sg.Themes.FourColors.SinCity.col3)

        if e == "5":
            self.throw_event()

### Layout ###
my_frame = sg.Frame([
    [
        grid := sg.GridFrame([
            [tex := sg.T("Hi", width=30), sg.VSep(), sg.T("World")],
            [sg.HSep() for i in range(4)],
            [
                sg.T("World",expand_y=True, relief= "sunken", expand=False),
                sg.VSep(),
                sg.T("Hi"),
                sg.Listbox(range(15), key="LB", default_event=True),
            ],
            [
                sg.Table(),
                sg.Combo(("Hi", "World"))
            ]
        ], alignment= "right").bind_event(sg.Event.MouseEnter, key= "Mouse Enter")
    ]
])

def custom_loop(e,v):
    print("Custom", e, v)

def periodic_event():
    n = 0
    while True:
        time.sleep(1)
        baseHandler.throw_event("Hi", n)
        n += 1

baseHandler = sg.BaseKeyHandler(custom_loop)

layout = [
    [
        sg.Input("Hallo Welt", key="In", default_event= True),
        subLay := sg.SubLayout(my_frame, custom_loop)
    ],[
        ButtonMat()
    ]
]

w = sg.Window(layout, grab_anywhere=True)
#w.update(background_color = "green")

### Additional configurations/actions ###
threading.Thread(target=periodic_event, daemon= True).start()

### Main loop ###
for e,v in w:
    print("Main Loop", e, v)


### After window was closed ###
