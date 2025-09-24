import threading
import time

import SwiftGUI as sg
import tkinter as tk

sg.Themes.FourColors.DarkGold()  # Use a different theme, as you please
#sg.Examples.preview_all_elements()
#sg.Examples.preview_all_themes()

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


w = sg.Window(layout, padx=50, pady=50)

sl = sg.SubWindow(toplevel_layout, padx= 50, pady= 50, event_loop_function=tl_eventloop, grab_anywhere=True)
sl2 = sg.SubWindow(first_layout, padx= 50, pady= 50, event_loop_function=tl_eventloop, grab_anywhere=True)
#sl.root.grab_set()

def blinker():
    while True:
        time.sleep(1)
        w.throw_event(key= "Test", value="Hallo")

#threading.Thread(target=blinker, daemon=True).start()
#print(sg.Popups.VirtualKeyboard.popup_virtual_keyboard())

for e,v in w:
    print(e,v)

