import SwiftGUI as sg

TooltipText = sg.T.with_go(sg.GlobalOptions.Tooltip)

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
        layout = [
            [
                TooltipText(    # Options of this text are defined in GlobalOptions.Tooltip
                    tooltip_text,
                )
            ]
        ]

        return layout


sg.Tooltips.set_tooltip_function(TooltipPopup)

