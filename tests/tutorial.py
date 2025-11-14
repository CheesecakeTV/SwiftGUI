import SwiftGUI as sg

sg.Themes.FourColors.DeepSea()

@sg.call_periodically(counter_reset= 0, autostart= False)
def count(counter):
    my_text.value = str(counter)

layout = [
    [
        my_text := sg.Text("0")
    ]
]

w = sg.Window(layout, padx=30, pady=30)
count()

for e, v in w:
    print(e, v)

