from itertools import batched, starmap, chain

import SwiftGUI as sg
from SwiftGUI import Color,font_windows


def preview_all_colors() -> None:
    """
    Have a look at all possible colors
    :return: 
    """ # Todo: Align colors vertically, not horizontally

    layout = [
        [
            sg.Input(width=5, background_color=getattr(Color, name)),
            sg.T(name,width=20,justify="right"),
            #sg.T(width=10)
        ] for name in dir(Color) if not name.startswith("_")
    ]

    layout = starmap(chain,batched(layout, 8))  # Just wanted to show of my itertools-skills

    w = sg.Window(layout)

    w.loop()

def preview_all_fonts_windows() -> None:
    """
    Have a look at all possible fonts on Windows
    :return:
    """
    layout = [
        [
            sg.Input(text=name,fonttype=getattr(font_windows, name),readonly=True),
        ] for name in dir(font_windows) if not name.startswith("_")
    ]

    layout = starmap(chain,batched(layout, 8))  # Just wanted to show of my itertools-skills

    w = sg.Window(layout)

    w.loop_close()

def preview_all_themes() -> None:
    """
    Have a look at all possible (prebuilt) themes
    :return:
    """
    layout = list()
    all_themes = sg.themes.__dict__.items()

    for n,(key,val) in enumerate(all_themes):
        if key.startswith("_"):
            continue

        sg.GlobalOptions.reset_all_options()
        val() # Apply theme

        layout.append([sg.Frame([
            [
                sg.T(f"Theme: {key}"),
            ],[
                sg.T("Input:",width=18),
                sg.Input("Hello!"),
            ],[
                sg.T("Disabled Input:",width=18),
                sg.Input("Hello, I'm readonly!",readonly=True),
            ],[
                sg.Check("Button clicked!",key=f"c{key}"),
                sg.Button("Click me, please!",key_function=sg.KeyFunctions.set_value_to(True,f"c{key}")),
            ]
        ],tk_kwargs={"padx":50,"pady":50})])


    sg.Window(layout).loop_close()
