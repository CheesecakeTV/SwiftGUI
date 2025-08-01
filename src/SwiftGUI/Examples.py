from itertools import batched, starmap, chain
from warnings import deprecated

import SwiftGUI as sg
from SwiftGUI import Color,font_windows


def preview_all_colors() -> None:
    """
    Have a look at all possible colors
    :return: 
    """

    layout = list()

    col = list()
    n = 0
    for _,name in enumerate(dir(Color)):
        if name.startswith("_"):
            continue

        col.append([
            sg.Input(width=5, background_color=getattr(Color, name)),
            sg.T(name, width=20, justify="right"),
        ])

        n += 1

        if n % 42 == 0:
            layout.append(sg.Frame(col))
            col = list()


    layout = [layout]

    w = sg.Window(layout)

    w.loop()

def preview_all_fonts_windows() -> None:
    """
    Have a look at all possible fonts on Windows
    :return:
    """
    layout = [
    ]

    n = 0
    for name in dir(font_windows):
        if name.startswith("_"):
            continue

        if n % 10 == 0:
            layout.append([])

        n += 1

        layout[-1].append(
            sg.Input(name,fonttype=getattr(font_windows, name),readonly=True),
        )


    w = sg.Window(layout)

    w.loop_close()

@deprecated("WIP")
def preview_all_themes() -> None:
    """
    Have a look at all possible (prebuilt) themes
    :return:
    """
    # Todo: This function sucks and I have no idea why...
    #  Suggestions are very welcome...

    layout = list()
    all_themes = sg.themes.__dict__.items()

    for n,(key,val) in enumerate(all_themes):
        if key.startswith("_"):
            continue

        sg.GlobalOptions.reset_all_options()
        val() # Apply theme

        layout.append([sg.Frame([
            [
                sg.T(f"Theme: {key}",font_underline=True),
            ],[
                sg.Spacer(height=10)
            ],[
                sg.T("Input:",width=18),
                sg.Input("Hello!"),
            ],[
                sg.T("Disabled Input:",width=18),
                sg.Input("Hello, I'm readonly!",readonly=True),
            ],[
                sg.Check("Button clicked!",key=f"c{key}"),
                sg.Button("Click me, please!",key_function=sg.KeyFunctions.set_value_to(True,f"c{key}")),
            ],[
                sg.Listbox(["Listbox","with","some","elements"],width=30,height=3)
            ]
        ],tk_kwargs={"padx":50,"pady":50})])


    sg.Window(layout).loop_close()
