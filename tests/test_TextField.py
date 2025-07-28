import random

import SwiftGUI as sg
import tkinter.ttk as ttk


layout = [
    [
        sg.Spacer(15),
        sg.Multiline("Das ist ein Text" * 15,key="ML",default_event=True,highlightthickness=5,highlightcolor="red",undo=True),
        sg.Spacer(15),
    ],[
        sg.Button("Event",key="Event"),
        sg.In(),
    ],[
        table := sg.Table(headings=["Hallo","Welt","Wie","Gehts?"], key="table", default_event=True, key_function=lambda val:val.__setitem__(0,"Clicked!"))
    ]
]


w = sg.Window(layout)

for i in range(5):
    table.append(["Hallo","Welt",i, "Letztes Feld!!!"])

table.index = 3
#table[5][1] = None
# table[5][0] = "Funktioniert!!!"
# table[5] += ["Hmmmm"]
# #del table[5][2]
# table[5] = [1,2,3]
# table.move(3,0)
# table.move_up(3,2)
# table.move_down(1,5)
table.swap(0,-1)

#table.insert_multiple([[n] for n in range(5)],2)

#w["tree"].selection = ('Test!', 'Hallo', 'Nächste Ebene')
#w["tree"].selection = None

for e,v in w:
    print(e,v)
    #del table[0]
    print(table.index, table.value)
    print("")

