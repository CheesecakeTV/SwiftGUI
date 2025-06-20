from collections.abc import Iterable
from SwiftGUI_LeButch import BaseElement, Frame, Text, Input


# Advanced / Combined elements

class Form(BaseElement):
    """
    Grid-Layout-Form with text-Input-combinations

    Still very WIP (of course), just a proof of concept
    """

    def __init__(
            self,
            texts:Iterable[str],
            key:any = "",
    ):
        self.key = key

        self.layout = [
            [
                Text(line),
                Input(key=key + line),
            ] for line in texts
        ]

        self._sg_widget = Frame(self.layout)


    def _personal_init(self):
        self._sg_widget._init(self,self.window)
        # for row in self.layout:
        #     for elem in row:
        #         elem._init(self._sg_widget,self.window)



