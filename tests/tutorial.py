import SwiftGUI as sg

layout = [
    [
        sg.Example(key="MyText",text="It does work..."),
    ],[
        sg.Button(text="Generate event",key="Hi")
    ]
]

w = sg.Window(layout)
print(w.loop()) # 'MyText': 'It does work...'
print(w["MyText"].value)    # This works too
w["MyText"].value = "Changed!"  # Value changes next time w.loop() is called
w.loop()
