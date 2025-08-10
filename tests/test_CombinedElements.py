import SwiftGUI as sg

class test(sg.BaseCombinedElement):

    def __init__(self):

        frame = sg.Frame([[
            sg.Radio("Test", default_event=True, key_function=self.throw_event),
            sg.Button("Hallo", key_function=self.throw_event),
            sg.T("Welt"),
        ]])

        super().__init__(frame, "Key")


layout = [
    [
        test()
    ]
]


w = sg.Window(layout)

for e,v in w:
    print(e,v)
