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
        sg.Table(headings=["Hallo","Welt","Wie","Gehts?"], key="table", default_event=True, key_function=lambda val:val.__setitem__(0,"Clicked!"))
    ]
]


w = sg.Window(layout)
table = w["table"]

for i in range(15):
    table.append(["Hallo","Welt",i, "Letztes Feld!!!"])

for k in range(5):
    table.insert(["Element","Sniper",k],random.randint(0,15))

table.selection = 5
#table[5][1] = None
table[5][0] = "Funktioniert!!!"
table[5] += ["Hmmmm"]
#del table[5][2]
table[5] = [1,2,3]

#table.insert_multiple([[n] for n in range(5)],2)

#w["tree"].selection = ('Test!', 'Hallo', 'Nächste Ebene')
#w["tree"].selection = None

for e,v in w:
    print(e,v)
    #del table[0]
    print(table.value)
    print("")

