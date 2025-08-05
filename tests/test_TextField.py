import random
from pprint import pprint

import SwiftGUI as sg
import tkinter.ttk as ttk

from SwiftGUI import Color

#sg.Themes.Hacker()
#sg.Themes.FacebookMom()

layout = [
    [
        sg.Spacer(15),
        sg.Multiline("Das ist ein Text" * 15,key="ML",default_event=True,highlightthickness=5,highlightcolor="red",undo=True),
        sg.Spacer(15),
    ],[
        sg.Button("Event",key="Event"),
        sg.Button("Append",key="Append"),
        sg.In(),
    ],[
        #table := sg.Table(headings=["Hallo","Welt","Wie","Gehts?"], key="table", default_event=True, key_function=lambda val:val.__setitem__(0,"Clicked!")),
        table := sg.Table(
            ((i,random.randint(10000,100000), "123456789_123456789", "") for i in range(15)),
            headings=["Hallo", "Welt", "Wie", "Gehts?"],
            key="table",
            default_event=True,
            column_width=12,
            background_color_rows = "lightblue",
            background_color_active_rows = "red",
            background_color= Color.orange_red,
            background_color_headings= "yellow",
            background_color_active_headings = "green",
            text_color_active="lime",  # Most nasty color-choices of them all...
            text_color=Color.navy,
            text_color_headings=Color.cadet_blue,
            text_color_active_headings="white",
            selectmode="extended",
        ).sort(1)
    ],[
        sg.TKContainer(ttk.Button, text = "Hallo Welt")
    ],[
        sg.HSep()
    ],
    [
        sg.Table(
            (("Hi","Welt") for i in range(5))
        ),
        sg.Spacer(25),
        sg.VSep()
    ]
]

w = sg.Window(layout)
table.sort(0)
table.all_indexes = 0, 5, 2
table.filter(lambda a:a % 2 == 0, by_column=0)
#table.filter(lambda a:a % 3 == 0, by_column=0)

s = w.ttk_style

for e,v in w:
    print(e,v)
    #del table[0]
    print(table.index, table.value)
    print(table.all_indexes)
    print(table.all_values)
    print()

    if e == "Append":
        table.clear_whole_table()

    if e == "Event":
        table.reset_filter()
    #table.overwrite_table([[i] for i in range(15)])

