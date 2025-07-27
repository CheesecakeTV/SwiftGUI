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
        sg.Table(headings=["Hallo","Welt","Wie","Gehts?"], key="table", default_event=True)
    ]
]


w = sg.Window(layout)
table = w["table"]

for i in range(15):
    table.append(["Hallo","Welt",i])

table.selection = 5

#w["tree"].selection = ('Test!', 'Hallo', 'Nächste Ebene')
#w["tree"].selection = None

for e,v in w:
    print(e,v)
    print(table.value)

