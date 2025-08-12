import SwiftGUI as sg

layout = [
    [
        lb := sg.Listbox(
            range(50),
            default_event=True,
            key="LB"
        )
    ],[
        sg.Button("Event", key="Event")
    ]
]



w = sg.Window(layout)
lb.color_row(3, background_color=sg.Color.light_blue)

for e,v in w:
    print(e,v)
    lb.value = "Click!"
    print(lb.value)

