#from itertools import batched
from SwiftGUI.Compat import batched
import SwiftGUI as sg

def preview_all_themes() -> None:
    """
    Have a look at all possible (prebuilt) themes
    :return:
    """
    layout = list()

    for n,(key,val) in enumerate(sorted(list(sg.Themes.all_themes.items()))):
        if key.startswith("_"):
            continue

        # Todo: Remove this
        if key == "Hacker":
            continue

        sg.GlobalOptions.reset_all_options()
        val() # Apply theme
        sg.GlobalOptions.Common_Textual.fontsize = 8
        sg.GlobalOptions.Button.fontsize = 8

        layout.append(sg.Frame([
            [
                sg.T("Theme: "),
                sg.T(f"{key}").bind_event(sg.Event.ClickLeft, key_function= lambda val: print(val)),
            ],[
                sg.HSep()
            ],[
                sg.Input("Hello!"),
            ],[
                sg.Input("Hello, I'm readonly!",readonly=True),
            ],[
                sg.HSep()
            ], [
                sg.LabelFrame([
                    [
                        sg.Check("I like it!"),
                        sg.Button("Take a closer look", key = key),
                    ], [
                        sg.Listbox(["Listbox", "with", "some", "elements", "and", "a scrollbar"], width=15, height=3, scrollbar=True),
                        sg.VSep(),
                        sg.TextField("TextField", width=15, height=3, scrollbar=False)
                    ]
                ], text= "LabelFrame")
            ]
        ], apply_parent_background_color= False))

    layout = batched(layout, 7)

    sg.GlobalOptions.reset_all_options()
    sg.Themes.FourColors.HotAsh()
    layout = [
         [
             sg.T("Click on the title of any theme and it will be printed to the console", fontsize= 14, expand= True)
         ]
    ] + list(layout)

    w = sg.Window(layout, title="Preview of all elements", alignment="left")

    for e,v in w:
        sg.GlobalOptions.reset_all_options()
        sg.Themes.all_themes[e]()
        sg.Examples.preview_all_elements(include_images= False)

