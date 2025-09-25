import SwiftGUI as sg

sg.Themes.FourColors.SinCity()

# This is my test for a planned combined element: A list with a search-bar

layout = [
    [
        my_in := sg.Input(
            key= "In",
            default_event= True,
        )
    ]
]

w = sg.Window(layout)

prev_text = ""
for e,v in w:
    print(e, v)

    if e == "In":
        if not my_in.value.startswith(prev_text):
            # If combined with a filter-list/table, you'd have to reset the filter here
            print("Neu filtern!")

        prev_text = my_in.value

