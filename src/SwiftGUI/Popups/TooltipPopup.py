import SwiftGUI as sg

class TooltipPopup(sg.BasePopupNonblocking):

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
        layout = [
            [
                sg.T(
                    tooltip_text,
                    background_color=sg.GlobalOptions.Common_Field_Background.single("background_color"),
                )
            ]
        ]

        return layout


sg.Tooltips.set_tooltip_function(TooltipPopup)
