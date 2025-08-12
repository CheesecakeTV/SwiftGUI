import SwiftGUI as sg

layout = [
    [
        sg.Form(
            ("Name", "Birthday", "Organization", "Favorite Food"),
            key = "Form",
            submit_button= True,
            big_clear_button= True,
        )
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(v["Form"])
