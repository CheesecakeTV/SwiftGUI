import SwiftGUI as sg
from SwiftGUI import Color

#sg.GlobalOptions.Button.fontsize = 12

class _virtual_keyboard:
    """
    I know this looks like a mess, and it is, but it's just a proof of concept for now.
    I'll clean it up later, pinky promise!
    """

    rows_default = [
        "^1234567890ß´",
        "qwertzuiopü+",
        "asdfghjklöä#",
        "<yxcvbnm,.-"
    ]

    rows_caps = [
        "°!\"§$%&/()=?`",
        "QWERTZUIOPÜ*",
        "ASDFGHJKLÖÄ'",
        ">YXCVBNM;:_"
    ]

    rows_special_chars = [
        r"•   Ω₿⌂{[]}\¿",
        r"@∩€∆∑√∞≈←→ ~",
        r"¼½¾ »«£₩¥☺█░",
        r"|♠♣♥♦♪♫▲►▼◄"
    ]

    def __init__(
            self,
            text: str = "",
            multiline: bool = False,
    ):
        # background_normal = sg.GlobalOptions.Button.single("background_color", None, "white")
        # background_active = sg.GlobalOptions.Button.single("background_color_active", None, Color.light_blue)
        repeat_kwargs = {
            "repeatdelay": 300,
            "repeatinterval": 100,
        }

        layout:list = list()
        for n, row in enumerate(self.rows_default):
            layout.append([])
            for m, char in enumerate(row):
                layout[-1].append(
                    sg.Button(
                        #char,
                        key = (n, m),
                        width= 2,
                        **repeat_kwargs,
                    )
                )

        self.buttons = layout.copy()

        _get_button = lambda a:sg.Button(a, key= a)

        # Special buttons
        layout[0].append(
            sg.Button(
                "◄──",
                key= "Backspace",
                **repeat_kwargs,
            )
        )
        layout[1] = [_get_button("Tab")] + layout[1]
        layout[2] = [
                        sg.Checkbox(
                            "Caps",
                            check_type= "button",
                            key= "Caps",
                            default_event= True,
                        )
                    ] + layout[2]
        if multiline:
            layout[2].append(_get_button("⏎"))

        layout[3] = [
                        sg.Checkbox(
                            "Shift",
                            check_type= "button",
                            key= "Shift",
                            default_event=True,
                        )
                    ] + layout[3] + [
                        sg.Button(
                            "Done",
                            key= "Done",
                        ),
                    ]

        layout.append([
            sg.Checkbox(
                "Special",
                check_type= "button",
                key= "Special",
                default_event=True,
            ),
            sg.Button(
                "Spacebar",
                key= "Spacebar",
                expand=True,
                **repeat_kwargs,
            ),
            sg.Button(
                "Cancel",
                key="Cancel",
            ),
        ])

        # Text-line
        if multiline:
            elem = sg.TextField(
                text,
                #expand= True,
                scrollbar= True,
                height= 5,
                width= 40,
            )
        else:
            elem = sg.Input(
                text,
                expand= True
            )

        layout = [[
            elem,
        ]] + layout

        self.input = elem

        _return = text
        def loop(e,v):
            nonlocal _return
            # print(e,v)

            if isinstance(e, tuple):
                self.char(self.buttons[e[0]][e[1]].value)
                if w["Shift"].value:
                    self.use_charmap(self.rows_default)
                    w["Shift"].value = False

            match e:
                case "Tab":
                    self.char("\t")

                case "Shift":
                    w["Caps"].value = False
                    w["Special"].value = False
                    if w["Shift"].value:
                        self.use_charmap(self.rows_caps)
                    else:
                        self.use_charmap(self.rows_default)

                case "Caps":
                    w["Shift"].value = False
                    w["Special"].value = False
                    if w["Caps"].value:
                        self.use_charmap(self.rows_caps)
                    else:
                        self.use_charmap(self.rows_default)

                case "Special":
                    w["Shift"].value = False
                    w["Caps"].value = False
                    if w["Special"].value:
                        self.use_charmap(self.rows_special_chars)
                    else:
                        self.use_charmap(self.rows_default)

                case "Spacebar":
                    self.char(" ")

                case "Backspace":
                    if self.input.value:
                        self.input.value = self.input.value[:-1]

                case "Done":
                    _return = self.input.value
                    w.close()

                case "Cancel":
                    w.close()

        w = sg.SubWindow(layout, title="Keyboard", alignment="left", keep_on_top=True, event_loop_function= loop)

        self.use_charmap(self.rows_default)

        w.block_others_until_close()
        self.rreturn = _return

    def use_charmap(self, charmap: list[str]):
        for b_row, c_row in zip(self.buttons, charmap):
            for button, char in zip(b_row, c_row):
                button.set_value(char)
            #map(lambda a:a[0].set_value(a[1]), zip(b_row, c_row))

    def char(self, char: str):
        self.input.value = self.input.value + char

def virtual_keyboard(
        text: str = "",
        multiline: bool = False,
):
    return _virtual_keyboard(
        text= text,
        multiline= multiline,
    ).rreturn







