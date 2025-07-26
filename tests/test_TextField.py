import SwiftGUI as sg
import tkinter.ttk as ttk

sg.Examples.preview_all_themes()
exit()

layout = [
    [
        sg.Spacer(15),
        sg.Multiline("Das ist ein Text" * 15,key="ML",default_event=True,highlightthickness=5,highlightcolor="red",undo=True),
        sg.Spacer(15),
    ],[
        sg.Button("Event",key="Event"),
        sg.In(),
    ],[
        sg.Treeview(headings=["Hallo","Welt","Wie","Gehts?"], key="tree")
    ]
]



w = sg.Window(layout)
w["tree"].selection = ('Test!', 'Hallo', 'Nächste Ebene')
#w["tree"].selection = None

for e,v in w:
    print(e,v)
    print(w["tree"].value)

