from typing import Iterable, Callable

from SwiftGUI.Validate import BaseValidateValue

class CanConvertTo(BaseValidateValue):

    def __init__(
            self,
            *types: type,
            allow_empty: bool = True,
            exception: type[BaseException] = ValueError,
    ):
        """
        Valid, if the value can be converted to ANY passed type
        :param types: Types to convert into
        :param allow_empty: True, if the value is allowed to be an empty string
        :param exception: This exception will be checked. You can almost always leave it ValueError. If not, change it to Exception.
        :param validate_backend_change:
        """
        self._types = types
        self._allow_empty = allow_empty
        self._exception = exception

        super().__init__()

    def is_valid_full_value(self, val: str) -> bool:
        if self._allow_empty and not val:
            return True

        return any(map(lambda a:self._can_convert_to(val, a), self._types))

    def _can_convert_to(self, val: str, this_type: type) -> bool:
        try:
            this_type(val)
        except self._exception:
            return False

        return True

class MaxLength(BaseValidateValue):

    def __init__(self, max_len: int):
        """
        The value can not be longer than max_len characters
        :param max_len:
        """
        self._max_len = max_len
        super().__init__()

    def is_valid_full_value(self, val: str) -> bool:
        return len(val) <= self._max_len

class ForbidDeletions(BaseValidateValue):
    def is_valid_deletion(self, val: str, val_before: str, deleted_val: str) -> bool:
        return False

class ForbidInsertions(BaseValidateValue):
    def is_valid_insertion(self, val: str, val_before: str, inserted_val: str) -> bool:
        return False

class WhitelistCharacters(BaseValidateValue):
    def __init__(self, characters: Iterable[str]):
        """
        Forbid every character not passed.
        Case sensitive
        :param characters:
        """
        self._chars = set(characters)
        super().__init__()

    def is_valid_insertion(self, val: str, val_before: str, inserted_val: str) -> bool:
        return all(map(lambda a:a in self._chars, inserted_val))

class FullValueFunction(BaseValidateValue):
    def __init__(self, function: Callable[[str], bool]):
        self._fct = function
        super().__init__()

    def is_valid_full_value(self, val: str) -> bool:
        return self._fct(val)


