from typing import Hashable, Any
import SwiftGUI as sg

# Only for the typehint. You can leave these out
from SwiftGUI import ValueDict
from SwiftGUI.Compat import Self

sg.Themes.FourColors.Jungle()

class ToggleButton(sg.BaseCombinedElement):
    def __init__(
            self,
            normal_text: str = "",  # Text when the button is "off"
            active_text: str = "",  # Text when the button is "on"

            key: Hashable = None,
            key_function = None,
    ):
        layout = [
            [
                my_button := sg.Button(
                    normal_text,
                    key = "Button",
                )
            ]
        ]

        self.button = my_button # Save the button and its texts for later
        self._normaltext = normal_text
        self._activetext = active_text

        super().__init__(   # Create the combined element
            layout,
            key= key,   # Key and key_function are handled automatically
            key_function= key_function,
        )

    def init_window_creation_done(self):
        """Called when the window is created"""

        # We don't want to destroy the theme, so let's read the values of these options
        # get_option only works when the window exists, so we do that in init_window_creation_done
        self._activecolor = self.button.get_option("background_color_active")
        self._activetextcolor = self.button.get_option("text_color_active")

    _my_value = False
    def _event_loop(self, e: Any, v: ValueDict):
        """Inner event-loop for the element"""
        if e == "Button":   # This is always True, since the button is the only contained element

            if self._my_value:  # If button is currently "active"
                self.button.update_to_default_value("background_color") # Reset these values to their defaults
                self.button.update_to_default_value("text_color")
                self.button.update_to_default_value("relief")
                self.button.value = self._normaltext    # Reset the text to normal
                self._my_value = False   # I am now inactive/False
            else:   # If button is currently "inactive"
                self.button.update(background_color = self._activecolor)    # Set these values to their active texts
                self.button.update(text_color  = self._activetextcolor)
                self.button.update(relief = "sunken")   # Make the button look "held down"
                self.button.value = self._activetext    # Update the text
                self._my_value = True   # I am now active/True

            # Cause an event in the actual event-system
            # Doesn't trigger on ".value = ..." for complicated reasons.
            # This is something you don't know, but just test/adjust until it works
            self._throw_event()

    def _get_value(self) -> bool:
        """Overwrite .value"""
        return self._my_value   # .value is "my" current state

    def set_value(self, val:bool) -> Self:
        """Overwrite .value"""
        if val != self._my_value:   # If val is different, toggle the button
            self.button.push_once() # ...by simulating a button-press

        return self

layout = [
    [
        ToggleButton(   # Use the combined element
            "Off",  # Text when normal
            "On",   # Text when active
            key="Toggle"
        )
    ],[
        sg.Spacer(height=10)
    ], [
        sg.Button("Turn on", key= "On")
    ],[
        sg.Button("Turn off", key="Off")
    ]
]

w = sg.Window(layout, padx= 50, pady= 50)

for e,v in w:
    print(e, v)

    if e == "On":
        w["Toggle"].value = True    # Push the toggle-button

    if e == "Off":
        w["Toggle"].value = False   # Un-push the toggle-button

    if e == "Toggle":
        print("The toggle-state is now", v["Toggle"])

