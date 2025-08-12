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
        form := sg.Form(
            [
                ("Hallo", "1"),
                ("Welt", "2"),
                ("Was geht?", "3")
            ],
            default_event=True,
            default_values=["Hai","Wie","Gehts"],
            key= "Form",
            submit_button= True,
            big_clear_button= True,
        )
    ]
]


w = sg.Window(layout)

for e,v in w:
    print(form.export_json())
