import SwiftGUI as sg

class test(sg.BaseCombinedElement):

    def __init__(self):

        frame = sg.Frame([[
            sg.Radio("Test", key="Button", default_event=True),
            sg.Button("Hallo"),
            sg.T("Welt"),
        ]])

        super().__init__(frame)


layout = [
    [
        test()
    ]
]


w = sg.Window(layout)

for e,v in w:
    print(e,v)
