
class Substitutions:
    action_code = "%d"  # 0 for deletion, 1 for insertion, -1 for focus or backend-change
    index = "%i"        # Index where a deletion/addition was attempted. -1 if none was attempted
    new_value = "%P"    # Value after the change, if allowed
    old_value = "%s"    # Value before the change
    changed_text = "%S" # The text that was inserted/deleted
    validate = "%v"     # This element's validate option
    callback_reason = "%V"  # The reason for this callback: 'focusin', 'focusout', 'key', or 'forced' if the text was changed from the backend
    widget_name = "%W"  # The name of the TKINTER-widget. This is not the element-key!!!

class BaseValidate:
    substitutions: tuple[str, ...] = tuple()    # https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/entry-validation.html

    def __iter__(self): # Generate the tuple that is passed to the tk.widget (after registering the function) later
        return iter((
            self.is_valid,
            *self.substitutions,
        ))

    def is_valid(self, *args) -> bool:
        """
        Overwrite this to specify the actual validation
        :return:
        """
        return True

class BaseValidateValue(BaseValidate):
    substitutions = (
        Substitutions.new_value,
        Substitutions.callback_reason,
    )

    def __init__(
            self,
            #validate_backend_change: bool = False,
    ):
        self._validate_backend_change = False   # This doesn't work...

    def is_valid(self, new_text: str, reason: str) -> bool:
        if (not self._validate_backend_change) and reason == "forced":
            return True

        return self.is_valid_value(new_text)

    def is_valid_value(self, val: str) -> bool:
        return True

    def __or__(self, other: "BaseValidateValue") -> "ValueUnion":
        return ValueUnion(self, other)

    def __and__(self, other: "BaseValidateValue") -> "ValueChain":
        return ValueChain(self, other)

class ValueChain(BaseValidateValue):

    def __init__(self, *validators: BaseValidateValue):
        """
        Is valid, if ALL passed validators passes the value-test
        :param validators:
        """
        self._validators = validators
        super().__init__()

    def is_valid_value(self, val: str) -> bool:
        return all(map(lambda a:a.is_valid_value(val), self._validators))


class ValueUnion(BaseValidateValue):

    def __init__(self, *validators: BaseValidateValue):
        """
        Is valid, if ANY passed validator passes the value-test
        :param validators:
        """
        self._validators = validators
        super().__init__()

    def is_valid_value(self, val: str) -> bool:
        return any(map(lambda a: a.is_valid_value(val), self._validators))

