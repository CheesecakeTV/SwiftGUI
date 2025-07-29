import random
from pprint import pprint

import SwiftGUI as sg
import tkinter.ttk as ttk

from SwiftGUI import Color

#sg.Themes.Hacker()

layout = [
    [
        sg.Spacer(15),
        sg.Multiline("Das ist ein Text" * 15,key="ML",default_event=True,highlightthickness=5,highlightcolor="red",undo=True),
        sg.Spacer(15),
    ],[
        sg.Button("Event",key="Event"),
        sg.In(),
    ],[
        #table := sg.Table(headings=["Hallo","Welt","Wie","Gehts?"], key="table", default_event=True, key_function=lambda val:val.__setitem__(0,"Clicked!")),
        table := sg.Table(
            headings=["Hallo", "Welt", "Wie", "Gehts?"],
            key="table",
            default_event=True,
        )#.bind_event(sg.Event.MouseEnter, key_function=lambda :print("Klappt"))
    ],[
        sg.TKContainer(ttk.Button, text = "Hallo Welt")
    ]
]

w = sg.Window(layout, ttk_theme="alt")

s = w.ttk_style
print(s.theme_names())

#s.theme_use("clam")
#pprint(s.layout("Treeview.Heading"))
#pprint(s.layout("Treeview.treearea"))

# pprint(s.layout("TButton"))
# print(s.element_options("TButton"))
# #s.configure("TButton.label",background = "red")
# s.configure("TButton.focus",background = "red")

# pprint(s.layout("TButton"))

#sg.Literals.relief

#table.update(background_color = "red")
# pprint(
#     #w.ttk_style.layout("TButton"),
#     w.ttk_style.element_options("Treeview.padding")
# )
#w.ttk_style.layout("Treeview", [("Treeview.field",{"border": 5})])
#table.update(background_color = sg.Color.cadet_blue)
#table.update(text_color = "red")


# pprint(w.ttk_style.layout("0.Treeview"))
# temp = w.ttk_style.layout("0.Treeview")
# temp[0][1]["border"] = 5
# #w.ttk_style.configure("0.Treeview.padding",sticky="n")
# w.ttk_style.layout("0.Treeview",temp)
# pprint(w.ttk_style.layout("0.Treeview"))


for i in range(50):
    table.append(["Hallo","Welt",i, "Letztes Feld!!!"])

#table.index = 3
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
    #table.overwrite_table([[i] for i in range(15)])

