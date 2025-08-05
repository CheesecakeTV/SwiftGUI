import SwiftGUI as sg


sg.GlobalOptions.Common_Textual.fontsize = 14

Tab1 = sg.Frame([
    [
        sg.T("This is a test"),
        sg.Spacer(width=15),
        sg.In()
    ],[
        sg.Button(
            "Event",
            key="Event",
            #expand_y=True,
            #expand=True,
        )
    ]
])

Tab2 = sg.Frame([
    [
        sg.T("This is another test"),
        sg.Spacer(width=15),
        sg.In(background_color=sg.Color.light_blue)
    ],[
        sg.T("Another frame, another tab")
    ],[
        sg.Button("Button", key="Button")
    ]
], key="Rechts", background_color="green")

layout = [
    [
        nb := sg.Notebook(
            Tab1,
            Tab2,
            tab_texts={"Links":"Left", None: "Noname"},
            padding=15,
            default_event=True,
            key="Notebook"
        ).bind_event_to_tab(tab_key="Rechts", key_function=lambda :print("FUNCTIONAL!!!"))
    ]
]

w = sg.Window(layout, "Notebook test", background_color=sg.Color.light_blue)
s = w.ttk_style

#Tab1.update(background_color = "lightgreen")

for e,v in w:
    print(e,v)
    print(nb.value)


