import re
from SwiftGUI.Validate import BaseValidateValue

class ReFullMatch(BaseValidateValue):

    def __init__(
            self,
            pattern: str,
    ):
        """
        The full value must match the passed regex-pattern
        :param pattern:
        """
        self._compiled = re.compile(pattern)
        super().__init__()

    def is_valid_full_value(self, val: str) -> bool:
        return bool(self._compiled.fullmatch(val))


