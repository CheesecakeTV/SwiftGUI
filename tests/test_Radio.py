import SwiftGUI as sg

#sg.Themes.Hacker()

#sg.GlobalOptions.Radiobutton.check_type = "button"
group = sg.RadioGroup()

layout = [
    [
        sg.Spinbox(
            key= "Spin",
            default_event= True,
            values= range(10)
            # number_min= 0,
            # number_max= 10,
            # increment= 0.5,
        )
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e,v)




