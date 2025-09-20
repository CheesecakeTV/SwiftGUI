import SwiftGUI as sg

sg.Themes.FourColors.Emerald()

def other_loop(e, v):
    print("Other loop:", e, v)

other_layoutpart = sg.LabelFrame([
    [
        sg.Button("Button1", key="Button1"),
        sg.Button("Button2", key="Button2"),
        sg.Button("Button3", key="Button3"),
    ]
], text= "Other layout-part")

layout = [
    [
        sg.SubLayout(
            other_layoutpart,
            event_loop_function= other_loop,
            key= "Sublayout"
        )
    ],[
        sg.Spacer(height= 15)
    ],[
        sg.Button("Button1", key="Button1"),
        sg.Button("Button2", key="Button2"),
        sg.Button("Button3", key="Button3"),
    ],[
        my_ml := sg.Multiline(undo=True)
    ],[
        sg.Table([[i] for i in range(15)]).see(-1)
    ]
]

w = sg.Window(layout, event_loop_function= other_loop)
w["Sublayout"]["Button2"].value = "Works like a charm!"

my_ml.append("Welt")
my_ml.append("Welt")
my_ml.append("Welt")
my_ml.append("Welt")

for e,v in w:
    print("Loop:", e, v)

