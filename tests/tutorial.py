import SwiftGUI as sg
import threading
import time

### Global options ###
sg.Themes.FourColors.SinCity()
#sg.Examples.preview_all_elements()
#sg.Examples.preview_all_themes()

test_vals = [[i] for i in range(100_000)]


### Layout ###
layout = [
    [
        table := sg.Table(  # table is a permanent reference to this object now
            headings=("Col1", "Col2", "Col3"),
        )
    ]
]

w = sg.Window(layout)

print(table.thread_running)
table.overwrite_table_threaded(test_vals)
print(table.thread_running)
#nb.value = "Harald"


### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    #print(nb.value)
    print(e,v)

    #v["Listbox"] = "Funktioniert"

### After window was closed ###
