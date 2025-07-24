import SwiftGUI as sg
from SwiftGUI import Color

# for _, name in enumerate(dir(sg.Color)):
#     if name.startswith("_"):
#         continue
#
#     print(f"{name} = \"{getattr(Color, name).replace(' ','')}\"")
#
# #sg.Examples.preview_all_colors()
# exit()

layout = [
    [
        sg.Spacer(15),
        sg.Multiline("Das ist ein Text" * 15,key="ML",default_event=True,highlightthickness=5,highlightcolor="red",undo=True),
        sg.Spacer(15),
    ],[
        sg.Button("Event",key="Event"),
        sg.In(),
    ]
]



w = sg.Window(layout)

for e,v in w:
    print(e,v)


