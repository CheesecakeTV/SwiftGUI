import SwiftGUI as sg

TooltipText = sg.T.with_go(sg.GlobalOptions.Tooltip)

class TooltipPopup(sg.BasePopupNonblocking):

    def __init__(
            self,
            tooltip_text: str,
            titlebar: bool = False,
            padx: int = 0,
            pady: int = 0,
            **window_kwargs,
    ):
        super().__init__(
            self._create_layout(tooltip_text),
            titlebar=titlebar,
            padx=padx,
            pady=pady,
            position= self._get_position(),
            **window_kwargs,
        )

    def _get_position(self) -> tuple[int, int]:
        posx, posy = sg.main_window().get_mouse_position_global()
        return posx + 15, posy

    def _create_layout(self, tooltip_text: str) -> list[list[sg.BaseElement]]:
        layout = [
            [
                TooltipText(    # Options of this text are defined in GlobalOptions.Tooltip
                    tooltip_text,
                )
            ]
        ]

        return layout


sg.Tooltips.set_tooltip_callable(TooltipPopup)

