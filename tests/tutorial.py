import threading
import time

import SwiftGUI as sg
import tkinter as tk

sg.Themes.FourColors.SlateBlue()  # Use a different theme, as you please

first_layout = [
    [
        sg.T("Still works", padding=150),
    ],[
        sg.Button("Buuuutton", key="Button")
    ]
]

# w = sg.Window(first_layout)
# for e,v in w:
#     print("First", e,v)

layout = [
    [
        sg.T("Test!", anchor="nw", relief="sunken", width=50, padding=15),
        sg.Button("Event", key="TestEvent")
    ]
]

toplevel_layout = [
    [
        sg.T("Toplevel!"),
        sg.ImageButton("Star.png", key= "Star")
    ]
]

def tl_eventloop(e, v):
    print("TL:",e,v)

#w = sg.Window(layout, padx=50, pady=50)

w = sg.Window(toplevel_layout, padx= 50, pady= 50, icon= "Star.png", event_loop_function=tl_eventloop)
sg.SubWindow(layout)

# tl = tk.Toplevel(w.root, padx=50)
# tl.title("Toplevel")
#
# fake_elem = sg.BaseElement()
# fake_elem._fake_tk_element = tl
# toplevel_layout._init(fake_elem, w)

def blinker():
    while True:
        time.sleep(1)
        w.throw_event(key= "Test", value="Hallo")

threading.Thread(target=blinker, daemon=True).start()

for e,v in w:
    print(e,v)
