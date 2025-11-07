import SwiftGUI as sg


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
