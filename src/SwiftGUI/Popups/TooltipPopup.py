import SwiftGUI as sg

class TooltipPopup(sg.BasePopupNonblocking):
    defaults = sg.GlobalOptions.Tooltip

    def __init__(
            self,
            tooltip_text: str,
    ):
        posx, posy = sg.main_window().get_mouse_position_global()
        super().__init__(
            self._create_layout(tooltip_text),
            titlebar=False,
            padx=0,
            pady=0,
            position= (posx + 15, posy),
        )

    def _create_layout(self, tooltip_text: str) -> list[list[sg.BaseElement]]:
        options = self.defaults.apply({   # These are defined via the global options
                "background_color": None,
                "relief": None,
                "padding": None,
                "text_color": None,
            }
        )

        layout = [
            [
                sg.T(
                    tooltip_text,
                    **options,
                )
            ]
        ]

        return layout


sg.Tooltips.set_tooltip_function(TooltipPopup)

