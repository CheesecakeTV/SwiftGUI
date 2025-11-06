import SwiftGUI as sg

### Global options ###
sg.Themes.FourColors.Emerald()
sg.Examples.preview_all_elements()
exit()

class Example(sg.BaseCombinedElement):
    def __init__(self):
        layout = [
            [
                sg.Button("Hi")
            ]
        ]

        super().__init__(
            layout,
        )

layout = [
    [
        Example()
    ]
]

w = sg.Window(layout)

for e,v in w:
    ...
