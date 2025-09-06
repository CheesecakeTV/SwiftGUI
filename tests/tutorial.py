import SwiftGUI as sg
import threading
import time

### Global options ###
sg.Themes.FourColors.SinCity()
#sg.Examples.preview_all_elements()
#sg.Examples.preview_all_themes()

def fkt():
    n = 0
    #my_fkt = w.get_event_function(me= w["An Event"], key="Custom key", key_function= lambda elem: elem.set_value(n))
    while True:
        time.sleep(1)
        w.throw_event(function= print, function_args= ("Hallo", "Welt"), function_kwargs= {"sep": " - "})
        n += 1

### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.Button("Hi, I'm an event", key="An Event")
    ]
]

w = sg.Window(layout)
#nb.value = "Harald"

threading.Thread(target= fkt, daemon= True).start()

### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    #print(nb.value)
    print(e,v)

    #v["Listbox"] = "Funktioniert"

### After window was closed ###
