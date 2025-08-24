from itertools import batched
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
                sg.T(f"Theme: {key}"),
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
                        sg.Listbox(["Listbox", "with", "some", "elements"], width=15, height=3, scrollbar=False),
                        sg.VSep(),
                        sg.TextField("TextField", width=15, height=3, scrollbar=False)
                    ]
                ], text= "LabelFrame")
            ]
        ], apply_parent_background_color= False))

    layout = batched(layout, 7)

    w = sg.Window(layout, title="Preview of all elements", alignment="left")

    for e,v in w:
        print(e)

        sg.GlobalOptions.reset_all_options()
        sg.Themes.all_themes[e]()
        sg.Examples.preview_all_elements(include_images= False)
