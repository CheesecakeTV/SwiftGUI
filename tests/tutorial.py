import SwiftGUI as sg
import threading
import time

### Global options ###
sg.Themes.FourColors.SinCity()
# sg.Examples.preview_all_elements()
# exit()

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
