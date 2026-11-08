
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
            self._callback,
            *self.substitutions,
        ))

    def _callback(self, *args) -> bool:
        """
        Overwrite this to specify the actual validation
        :return:
        """
        return True

class BaseValidateValue(BaseValidate):
    substitutions = (
        Substitutions.new_value,
        Substitutions.callback_reason,
        Substitutions.old_value,
        Substitutions.changed_text,
        Substitutions.action_code,
    )

    def __init__(
            self,
            #validate_backend_change: bool = False,
    ):
        self._validate_backend_change = False   # This doesn't work...

    def _callback(self, val: str, reason: str, val_before: str, changed_val: str, action_code: str) -> bool:
        """
        Gets called by tkinter.
        All checks must pass to allow the action.
        """
        if (not self._validate_backend_change) and reason == "forced":
            return True

        if action_code == "0":    # Deletion
            if not self.is_valid_deletion(val, val_before, changed_val):
                return False
        elif action_code == "1":  # Insertion
            if not self.is_valid_insertion(val, val_before, changed_val):
                return False

        return self.is_valid_full_value(val)

    def is_valid_full_value(self, val: str) -> bool:
        """Called on every check with the full value after the change"""
        return True

    def is_valid_insertion(self, val: str, val_before: str, inserted_val: str) -> bool:
        """Called when text is inserted by the user"""
        return True

    def is_valid_deletion(self, val: str, val_before: str, deleted_val: str) -> bool:
        """Called when text is deleted by the user"""
        return True

    def __or__(self, other: "BaseValidateValue") -> "Union":
        return Union(self, other)

    def __and__(self, other: "BaseValidateValue") -> "Chain":
        return Chain(self, other)

    def __neg__(self) -> "Negate":
        return Negate(self)

class Chain(BaseValidateValue):

    def __init__(self, *validators: BaseValidateValue):
        """
        Is valid, if ALL passed value-validators passes the value-test
        :param validators:
        """
        self._validators = validators
        super().__init__()

    def _callback(self, *args) -> bool:
        return all(map(lambda a: a._callback(*args), self._validators))


class Union(BaseValidateValue):

    def __init__(self, *validators: BaseValidateValue):
        """
        Is valid, if ANY passed value-validator passes the value-test
        :param validators:
        """
        self._validators = validators
        super().__init__()

    def _callback(self, *args) -> bool:
        return any(map(lambda a: a._callback(*args), self._validators))

class Negate(BaseValidateValue):
    def __init__(self, validator: BaseValidateValue):
        """
        Is valid, if the passed validator is not valid
        :param validator:
        """
        self._validator = validator
        super().__init__()

    def _callback(self, *args) -> bool:
        return not self._validator._callback(*args)

