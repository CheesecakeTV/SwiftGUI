import SwiftGUI as sg

#sg.Themes.Hacker()

#sg.GlobalOptions.Radiobutton.check_type = "button"
group = sg.RadioGroup()

layout = [
    [
        sg.Radio("Test", group= "Test", key="Test", default_event=True),
        test := sg.Radio("Test", group= "Test", key= "Test", default_event=True, default_value=True),
        sg.Radio("Test", group="Test", key="Test"),
        sg.Radio("Test", group="Test", key="Test"),
    ],[
        test1 := sg.Radio("Test", group="Test1", key="Test", default_event=True, default_value=True),
        sg.Radio("Test", group="Test1", key="Test", default_event=True, default_value=True),
        sg.Radio("Test", group="Test1", key="Test", default_event=True, default_value=True),
        sg.Radio("Test", group="Test1", key="Test", default_event=True, default_value=True),
    ],[
        sg.Radio("Hallo", group=group),
        sg.Radio("Hallo", group=group),
        sg.Radio("Hallo", group=group),
        sg.Radio("Hallo", group=group),
        sg.Radio("Hallo", group=group),
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(test.value, test1.value)




