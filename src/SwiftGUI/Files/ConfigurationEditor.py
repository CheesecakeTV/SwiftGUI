from typing import Hashable, Callable, Iterable, Any

from SwiftGUI import BaseCombinedElement, Form, Button, Notebook, ValueDict
from SwiftGUI.Extended_Elements.TabFrame import TabFrame
from SwiftGUI.Files import ConfigSection, ConfigFile
from SwiftGUI.Compat import Self

class ConfigSectionEditor(BaseCombinedElement):
    """
    A layout-element that can be used to edit a configuration-section directly
    """

    def __init__(
            self,
            config_section: ConfigSection,
            *,
            key: Hashable = None,
            key_function: Callable | Iterable[Callable] = None,
            default_event: bool = False,
            **form_kwargs,
    ):
        self._config_section = config_section
        values = config_section.defaults

        assert values, f"The configuration-section {config_section} does not have default values."

        layout = [
            [
                my_form := Form(
                    values.keys(),
                    **form_kwargs,
                ),
            ],[
                Button("Save", key_function= self.save),
                Button("Reset", key_function= self.reset)
            ]
        ]

        self.form = my_form

        super().__init__(
            layout,
            key = key,
            key_function= key_function,
            default_event= default_event,
        )

    def save(self) -> Self:
        self._config_section.set_many(**self.form.value)
        self._config_section.save()
        self.done(self.value)
        self.throw_default_event()
        return self

    def reset(self) -> Self:
        self.form.value = self._config_section.to_dict()
        self.done(self.value)
        self.throw_default_event()
        return self

    def from_json(self, *_) -> Self:
        """This element should not be loaded from a json-save"""
        return self

    def to_json(self, *_) -> None:
        """This element should not be saved to a json-save"""
        return None

    def _get_value(self) -> dict:
        return self._config_section.to_dict()

    def set_value(self, val:dict) -> Self:
        self.form.value = val
        self.save()
        return self

    def init_window_creation_done(self):
        self.form.value = self._config_section.to_dict()

class ConfigFileEditor(BaseCombinedElement):
    """
    A layout-element that can be used to edit all configuration-sections of a configuration-file at once
    """

    value: None

    def __init__(
            self,
            config_file: ConfigFile,
            *,
            key: Hashable = None,
            # key_function: Callable | Iterable[Callable] = None,
            # default_event: bool = False,
            # **form_kwargs,
    ):
        self.config_file = config_file

        self.tab_frames = [
            TabFrame(
                [[ConfigSectionEditor(section, key_function=self.throw_default_event, default_event=True)]],
                fake_key= name,
            ) for name, section in config_file.all_sections.items() if section.defaults
        ]

        layout = [
            [
                Notebook(
                    *self.tab_frames,
                )
            ]
        ]

        super().__init__(
            layout,
            key= key,
            # key_function= key_function,
            # default_event=default_event,
        )

    def _get_value(self) -> None:
        return None

    def set_value(self, val:Any) -> Self:
        return self



