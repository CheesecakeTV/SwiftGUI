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
            seperate_keys:bool=False,   # Key for every input
    ):
        self.key = key
        self.texts = texts

        self.layout = [
            [
                Text(line),
                Input(
                    key=key + line if seperate_keys else None
                ),
            ] for line in texts
        ]

        self._sg_widget = Frame(self.layout)

    def _personal_init(self):
        self._sg_widget._init(self,self.window)

    def _get_value(self) -> any:
        return {
            line:elem[1].value for line,elem in zip(self.texts,self.layout)
        }

