from typing import Hashable

import SwiftGUI as sg

sg.Themes.FourColors.DarkTeal()
sg.Popups.ListPicker(range(15))
exit()

class Example(sg.Popups.BasePopup, str):

    def __init__(self, question: str, fontsize: int = 12):
        layout = [
            [
                sg.T(question, fontsize=fontsize),
            ],[
                sg.Button("Yes", key="Yes", fontsize=fontsize),
                sg.Button("No", key="No", fontsize=fontsize)
            ]
        ]

        super().__init__(layout, default= "")

    def _event_loop(self, e: Hashable, v: sg.ValueDict):
        self.done(e)

answer: str = Example("How are you today?")
print("Answer:",answer)

exit()
main_layout = [
    [
        sg.Button(
            "Some Button",
            width= 30,
            height= 5,
            key= "Main Button",
        )
    ]
]

another_layout = [
    [
        sg.Input(key= "Input"),
        sg.Button("Button 1", key="B1"),
        sg.Button("Button 2", key="B2"),
        sg.Button("Button 3", key="B3"),
    ]
]

def sw_loop(e,v):
    # Some example-loop
    print("Button-press:", e)
    print("Input-value:", v["Input"])
    sw["Input"].value = e

w = sg.Window(main_layout)
sw = sg.SubWindow(another_layout, event_loop_function=sw_loop)

w.loop()

