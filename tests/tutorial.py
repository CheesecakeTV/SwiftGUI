import SwiftGUI as sg
import SwiftGUI.Canvas_Elements as sgc
import cProfile

#sg.Themes.FourColors.Emerald()
print(cProfile.run("sg.Examples.preview_all_fonts_windows()", sort=0))
exit()

layout = [
    [
        sg.Text("Hide example")
    ],[
        sg.T("Maybe some hidden button?"),
        my_button := sg.Button(
            "Hide me!",
            key="Ev",
        ),
        sg.T("Seems to work suspiciously well...?")
    ],[
        sg.Button("Hide", key="Hide"),
        sg.Button("Show", key="Show")
    ]
]

w = sg.Window(layout)

for e,v in w:
    print(e) # Text

    #print(my_button.tk_widget.pack_info())
    if e == "Hide":
        my_button.hide()
    if e == "Show":
        my_button.show()

