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
            sg.In(width=5, background_color=getattr(Color, name)),
            sg.Button(
                name,
                fontsize=7,
                width=20,
                justify="right",
                key_function=lambda elem, w: [print(elem.value),
                                              w._update_initial(background_color=getattr(Color, elem.value))],
                fonttype=font_windows.Small_Fonts
            ),
        ])

        n += 1

        if n % 42 == 0:
            layout.append(sg.Frame(col))
            layout.append(sg.Spacer(15))
            col = list()


    layout = [
        [
            sg.T("Click on any text to print it to console", fontsize=16)
        ],
        layout
    ]

    sg.SubWindow(layout, title="SwiftGUI color-preview").block_others_until_close()

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


    w = sg.SubWindow(layout)

    w.block_others_until_close()

