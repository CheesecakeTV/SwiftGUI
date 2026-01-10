import pickle
from abc import abstractmethod
from pathlib import Path
from typing import Hashable, Any, Iterable
import json

from SwiftGUI.Compat import Self
from SwiftGUI.GlobalOptions import DEFAULT_OPTIONS_CLASS


class DictFileOptions(DEFAULT_OPTIONS_CLASS):
    add_defaults_to_values: bool = False
    auto_save: bool = True

class BaseDictFile:
    """
    Derive this class to create your own dict-file-handler.
    This is very easy.
    Just look at the two classes at the bottom of this file to know how it's done.
    """

    def __init__(
            self,
            path: str | Path,
            *,
            defaults: dict = None,
            add_defaults_to_values: bool = None,
            auto_save: bool = None,
    ):
        self._values = dict()   # Stores the actual values

        #self._path = Path(path)
        self.path = path

        self._add_defaults_to_values = DictFileOptions.single("add_defaults_to_values", add_defaults_to_values)

        self._defaults: dict = dict(defaults) if defaults else dict()

        self.auto_save = DictFileOptions.single("auto_save", auto_save)

        self.load()

        if defaults:
            self.add_defaults_dict(defaults)

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, val: str | Path):
        self._path = Path(val)

        self._path.parent.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def _save_to_file(
            self,
            values: dict,
            path: Path,
    ):
        """Pure save-operation"""
        pass

    def save(
            self,
            save_to: str | Path = None,
    ) -> Self:
        """
        Save the file
        :param save_to: Path. Leave empty to use normal file-path
        :return:
        """
        if save_to:
            save_to = Path(save_to)
        else:
            save_to = self._path

        self._save_to_file(self._values, save_to)

        return self

    def _do_auto_save(self):
        """Save if auto-save is on"""
        if self.auto_save:
            self.save()

    @abstractmethod
    def _load_from_file(
            self,
            path: Path
    ) -> dict:
        """
        Pure load-operation

        return the values as a dictionary
        """
        pass

    def load(
            self,
            load_from: str | Path = None,
            add_defaults_to_value: bool = None,
    ) -> Self:
        if load_from:
            load_from = Path(load_from)
        else:
            load_from = self._path

        if load_from.exists():
            self._values = self._load_from_file(load_from)

        if add_defaults_to_value is None:
            add_defaults_to_value = self._add_defaults_to_values
        if add_defaults_to_value:
            self.add_defaults_dict(self._defaults, add_to_values=True)

        return self

    def get(self, key: Hashable, default: Any = None) -> Any:
        if not key in self:
            return self._defaults.get(key, default)

        return self._values.get(key)

    def __getitem__(self, item: Hashable) -> Any:
        if not item in self:
            return self._defaults[item]

        return self._values[item]

    def __contains__(self, item: Hashable) -> bool:
        return item in self._values

    def __setitem__(self, key, value):
        self.set(key, value)

    def set(self, key: Hashable, value: Any) -> Self:
        """
        Overwrite a single value
        Same as ...[key] = value
        :param key:
        :param value:
        :return:
        """
        self._values[key] = value
        self._do_auto_save()
        return self

    def set_many_dict(self, items: dict) -> Self:
        """
        Same as set_many, but allows for non-string keys
        """
        self._values.update(items)
        self._do_auto_save()
        return self

    def set_many(self, **items: Any) -> Self:
        """
        Set multiple values at once
        :param items:
        :return:
        """
        self.set_many_dict(items)
        return self

    def add_defaults_dict(self, defaults: dict, add_to_values: bool = None, add_to_these_values: dict = None) -> Self:
        """
        Same as add_defaults, but allows for non-string keys
        :param add_to_these_values: This dict will be updated instead of the actual values
        :param add_to_values:
        :param defaults:
        :return:
        """
        if add_to_these_values is None:
            add_to_these_values = self._values

        not_contained = set(defaults.keys()).difference(set(add_to_these_values.keys()))

        self._defaults.update(defaults)

        if (add_to_values is None and self._add_defaults_to_values) or add_to_values:
            add_to_these_values.update({
                key:defaults[key] for key in not_contained
            })

        return self

    def add_defaults(self, **defaults: Any) -> Self:
        """
        If the given values are not inside the file, they'll be set to the passed value
        :param defaults:
        :return:
        """
        self.add_defaults_dict(defaults)

        return self

    def to_dict(self) -> dict:
        """
        Return all values as a dictionary
        :return:
        """
        return self._values.copy()

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} at {id(self)}: {self._values}>"

    def delete_key(self, *keys: Hashable) -> Self:
        """
        Delete one or more keys/values from this file
        """
        for key in keys:
            if key in self._values:
                del self._values[key]

        if self._add_defaults_to_values:
            self.add_defaults_dict(self._defaults)

        self._do_auto_save()

        return self

    def __delitem__(self, key: Hashable):
        self.delete_key(key)

    def __iter__(self):
        return iter(self._values)

    def keys(self) -> Iterable[Hashable]:
        """Same as dict.keys()"""
        return self._values.keys()

    def values(self) -> Iterable[Any]:
        """Same as dict.values()"""
        return self._values.values()

    def items(self) -> Iterable[tuple[Hashable, Any]]:
        """Same as dict.items()"""
        return self._values.items()

class DictFileJSON(BaseDictFile):
    """
    A pseudo-dictionary that's saved in a json-file.
    Allows saving the "usual" python-types, including list, dict and set.
    Can also be used as a configuration-file, since it is readable.
    """

    def _save_to_file(self, values: dict, path: Path):
        path.write_text(json.dumps(values, indent=4))

    def _load_from_file(self, path: Path) -> dict:
        return json.loads(path.read_text())

class DictFilePickle(BaseDictFile):
    """
    A pseudo-dictionary that's saved in a pickle-file.
    Allows to save any kind of type, even selfmade ones.
    It even keeps references between saved objects intact!

    On the other hand, it's not humanly-readable.

    Keep in mind that pickle can cause issues with backward-compatability WHEN SAVING SELFMADE CLASSES and updating them after saving.
    """

    def _save_to_file(self, values: dict, path: Path):
        with path.open("wb") as f:
            pickle.dump(values, f)  # No idea why there is a warning here.

    def _load_from_file(self, path: Path) -> dict:
        with path.open("rb") as f:
            return pickle.load(f)


