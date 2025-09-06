import SwiftGUI as sg
import threading
import time

### Global options ###
sg.Themes.FourColors.SinCity()
#sg.Examples.preview_all_elements()
#sg.Examples.preview_all_themes()

test_vals = [[i] for i in range(100_000)]


### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        table := sg.Table(
            headings= ["Test"],
        ).insert_multiple_threaded(test_vals, delay= 0.3),
    ]
]

w = sg.Window(layout)
#nb.value = "Harald"


### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    #print(nb.value)
    print(e,v)

    #v["Listbox"] = "Funktioniert"

### After window was closed ###
