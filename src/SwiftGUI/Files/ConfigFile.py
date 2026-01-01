import configparser
import json
from functools import partial
from os import PathLike
from pathlib import Path
from typing import Any

from SwiftGUI.Compat import Self

# You might think this is redundant when there is configparser, but I find my classes more convenient.
# If you don't, feel free to use whatever you like :D

class ConfigSection:

    def __init__(
            self,
            name: str,
            file: "ConfigFile",
    ):
        self._name = name
        self.file = file

        self.defaults = dict()

        if not file.config.has_section(name):
            file.config[name] = dict()

        self.section: configparser.SectionProxy = file.config[name]

    def add_defaults(self, **defaults: str) -> Self:
        """
        If the given values are not inside the configuration file, they'll be set to the passed value
        :param defaults:
        :return:
        """
        before = self.to_dict()

        self.defaults.update(defaults)

        defaults.update(before)
        self.file.config.read_dict({
            self._name: defaults
        })

        if self.file.auto_save:
            after = self.to_dict()
            if before != after:
                self.file.save()

        return self

    def add_json_defaults(self, **defaults: Any) -> Self:
        """
        The json-variant of apply_defaults
        :param defaults:
        :return:
        """
        self.add_defaults(**self.json_dumps_many(defaults))
        return self

    def save(self, save_to: str | PathLike = None) -> Self:
        """
        Save the configuration to the file
        :return:
        """
        self.file.save(save_to)
        return self

    def load(self, load_from: str | PathLike = None) -> Self:
        """
        (Re-) load the (whole) file if it exists
        :param load_from: Can be used to import a different file
        :return:
        """
        self.file.load(load_from)
        return self

    def to_dict(self) -> dict:
        """
        Return all values as a dict.
        The reference is destroyed, so you may edit this dict without changing the file.
        """
        return dict(self.section)

    def set(self, key: str, value) -> Self:
        """
        Same as object_name[key] = value

        :param key: Parameter-name
        :param value: New value
        :return:
        """
        self.section[key] = str(value)

        if self.file.auto_save:
            self.file.save()

        return self

    def set_many(self, **values) -> Self:
        """
        Same as .set, but for multiple values at once

        :param values:
        :return:
        """
        keys = values.keys()
        values = map(str, values.values())  # Convert to string

        values = dict(zip(keys,values))

        self.file.config.read_dict({
            self._name: values
        })

        if self.file.auto_save:
            self.file.save()

        return self

    def set_json(self, key: str, value) -> Self:
        """
        Save a value as a json-string.
        This way it's possible to save and load lists/dicts.

        :param key:
        :param value:
        :return:
        """
        self.set(key, json.dumps(value, indent=4))
        return self

    @staticmethod
    def json_dumps_many(to_convert: dict) -> dict:
        """
        json-encode all values of a dictionary and RETURN IT AS A NEW DICT.
        The reference is lost.

        :param to_convert:
        :return:
        """
        keys = list(to_convert.keys())
        vals = list(
            map(
                partial(json.dumps, indent=4),
                to_convert.values()
            )
        )

        return dict(zip(keys, vals))

    def set_json_many(self, **values) -> Self:
        """
        Same as .set_json but for many values at once
        :param values:
        :return:
        """
        self.set_many(
            **self.json_dumps_many(values)
        )

        return self

    def __setitem__(self, key, value):
        self.set(key, value)

    def get(self, key: str, default: Any = None, to_type: type = None) -> Any:
        """
        Return the key.
        If the key is unavailable, return default

        :param default:
        :param key:
        :param to_type: Convert the return-value to this type
        :return:
        """
        ret = self.section.get(key, None)

        if ret is None:
            return self.defaults.get(key, default)

        if to_type is None:
            return ret

        try:
            return to_type(ret)
        except ValueError:
            return self.defaults.get(key, default)

    def get_int(self, key: str, default: Any = None) -> Any:
        return self.get(key, default, int)

    def get_float(self, key: str, default: Any = None) -> Any:
        return self.get(key, default, float)

    def get_bool(self, key: str, default: bool = False) -> bool:
        ret = self.get(key, None)
        if ret is None:
            return default

        return ret.strip().lower() in {"1", "true", "y", "yes"}

    def get_json(self, key: str, default: Any = None) -> Any:
        """
        Return the key.
        The value must have been set using .set_json
        If the key is unavailable, return default

        :param default:
        :param key:
        :return:
        """
        ret = self.section.get(key, None)

        if ret is None:
            return self.defaults.get(key, default)

        try:
            ret = json.loads(ret)
        except json.JSONDecodeError:
            return default

        return ret

    def __getitem__(self, item) -> str:
        return self.section[item]

class ConfigFile:

    # Todo: Prevent the user from creating multiple objects for the same file
    def __init__(
            self,
            path: str | PathLike,
            auto_save: bool = True,
            **configparser_kwargs,
    ):
        self.path: Path = Path(path)
        self.all_sections: dict[str, ConfigSection] = dict()

        self.auto_save: bool = auto_save    # Feel free to overwrite this

        configparser_kwargs["strict"] = configparser_kwargs.get("strict", False)

        self.config = configparser.ConfigParser(**configparser_kwargs)
        self.load()

    def load(self, load_from: str | PathLike = None) -> Self:
        """
        (Re-) load the file if it exists
        :return:
        """
        if load_from is None:
            load_from = self.path
        else:
            load_from = Path(load_from)

        if load_from.exists():
            with load_from.open("r") as f:
                self.config.read_file(f)

        return self

    def save(self, save_to: str | PathLike = None) -> Self:
        """
        Save the configuration to a file
        :param save_to: Leave this None to save to default location
        :return:
        """
        if save_to is None:
            save_to = self.path
        else:
            save_to = Path(save_to)

        with save_to.open("w") as f:
            self.config.write(f)

        return self

    def __getitem__(self, name: str) -> ConfigSection:
        """
        Return the section with the given name.
        If it doesn't exist, it is created.
        :param name:
        :return:
        """
        if not name in self.all_sections:
            self.all_sections[name] = ConfigSection(name, self)

        return self.all_sections[name]

    def section(self, name: str, defaults: dict = None, json_defaults: dict = None) -> ConfigSection:
        """
        Return the section with the given name.
        If it doesn't exist, it is created.

        Passed default-values are applied to the section

        :param json_defaults:
        :param name:
        :param defaults:
        :return:
        """
        new_section = self[name]

        if defaults:
            new_section.add_defaults(**defaults)

        if json_defaults:
            new_section.add_json_defaults(**json_defaults)

        return new_section


