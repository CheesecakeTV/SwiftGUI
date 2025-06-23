from itertools import batched, starmap, chain

import SwiftGUI as sg
from SwiftGUI import Color


def preview_all_colors() -> None:
    """
    Have a look at all possible colors
    :return: 
    """ # Todo: Align colors vertically, not horizontally

    layout = [
        [
            sg.Input(width=5,background_color=getattr(Color,name)),
            sg.T(name,width=20,justify="right"),
            #sg.T(width=10)
        ] for name in dir(Color) if not name.startswith("_")
    ]

    layout = starmap(chain,batched(layout, 8))  # Just wanted to show of my itertools-skills

    w = sg.Window(layout)

    w.loop()


