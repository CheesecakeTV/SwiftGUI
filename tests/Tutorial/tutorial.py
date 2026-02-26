import logging

import numpy as np
import SwiftGUI as sg
import itertools
import random
from enum import Enum
import sys
import SwiftGUI_Logging as sgl

sgl.Configs.exceptions_to_file("Crashlogs/Crash.log")

# If there are too many empty fields, the recursion-limit could crash the program.
# This is prevented by increasing the limit
sys.setrecursionlimit(10000)

sg.Themes.FourColors.FrostyBlue()

sg.Files.set_root("SwiftGUI Minesweeper")   # Define program-directory
_save_file = sg.Files.DictFileJSON(sg.Files.root_path("Values.json"))   # Define the save-file inside the program directory

# Custom element-flags
class CustomFlags(Enum):
    REVEALED = 100  # Field is revealed
    FLAGGED = 101   # Field is flagged indicating there is a bomb

# Create a custom popup-class
class Minesweeper(sg.BasePopupNonblocking):
    _colors = ( # Colors of the numbers in order
        "blue",
        "green",
        "red",
        "purple",
        "maroon",
        "cyan",
        "orange",
        "gray8",
    )

    def __init__(
            self,
            rows: int = 8,
            columns: int = 8,
            bomb_count: int = 10,
    ):
        # Empty field the size of rows x columns
        self._gamefield = np.zeros(shape=(rows, columns))

        # How many fields are left
        self._remaining_fields = rows * columns

        self._rows = rows
        self._colums = columns
        self._bomb_count = min(bomb_count, self._remaining_fields - 1)  # Limit how many bombs there are by the number of fields

        self._flag_count = 0    # How many fields are flagged (Just to show the value)

        # Pick k many random coordinates
        # Look up the documentation of itertools for details
        self._bombs = random.sample(  # self._bombs saves the coordinates of the bombs
            tuple(itertools.product(range(rows), range(columns))), k=self._bomb_count
        )

        list(map(self._add_bomb, self._bombs))  # Add the bombs

        self._buttons = [
            [
                sg.Button(
                    key = (r, c),   # The key is the "location" of that button  (row, column)
                    width= 2,
                    borderwidth=1,
                    key_function= self._click,
                ).bind_event(   # Bind right-click event
                    sg.Event.ClickRight,
                    key_function = self._rightclick,
                ) for c in range(columns)   # One button per column
            ] for r in range(rows)  # One list of buttons per row
        ]

        layout = self._buttons + [  # Add some more to the layout
            [
                sg.Spacer(height=5),
            ], [
                sg.T(f"Bombs: {self._bomb_count}"),
            ],[
                sg.T(f"Flags: "),
                sg.T("0", key= "Flags")
            ],[
                sg.Spacer(height=5),
            ], [
                sg.Button(
                    "Give up (Double-click)"
                ).bind_event(   # Only a double-click should cause an event
                    sg.Event.ClickDoubleLeft,
                    key_function= self._you_lost
                ),
            ]
        ]

        super().__init__(layout, title= f"Minesweeper with {self._remaining_fields} fields", padx= 15, pady= 15)

        # "Click" an empty field from the start so you don't hit a bomb from the beginning
        self._open_empty_field()

    def _open_empty_field(self):
        """
        "Click" a random free field
        """
        all_fields = list(itertools.product(range(self._rows), range(self._colums)))    # List all field-coordinates
        random.shuffle(all_fields)  # Shuffle that list

        for c in all_fields:    # Check each of that fields if it is empty
            if self._field_value(c) == 0:   # When an empty field is found, "click" it and stop searching
                self._click(c)
                return

    def _add_bomb(self, coordinate: tuple[int, int]):
        """
        Place a single bomb on the field by incrementing every field-number around it
        :param coordinate:  Where to place it
        :return:
        """
        for row, col in self._surrounding_fields(coordinate):   # Iterate through every surrounding field of the passed coordinate
            self._gamefield[row, col] += 1  # Increment the field's value

    def _click(self, e: tuple[int, int], elem: sg.Button = None):
        """
        Leftclick on a button
        """
        # If the passed element is flagged, don't do anything
        if elem is not None and elem.has_flag(CustomFlags.FLAGGED):
            return

        try:
            val = self._reveal_one(e)
        except RecursionError:  # _reveal_one can run recursively. With too many empty fields, the recursion-depth might exceed the limit.
            self.close()
            sg.Popups.show_text("There were too many empty fields.\nIncrease the number of bombs.")
            return

        if val == -1:   # Hit a bomb
            self._you_lost()
        elif self._remaining_fields == self._bomb_count:
            self._you_won()

    def _rightclick(self, elem: sg.Button):
        """
        Right-click: Add or remove a flag
        """
        if elem.has_flag(CustomFlags.REVEALED):
            return

        if elem.has_flag(CustomFlags.FLAGGED):
            elem.remove_flags(CustomFlags.FLAGGED)
            elem.value = ""
            self._flag_count -= 1
        else:
            elem.add_flags(CustomFlags.FLAGGED)
            elem.value = "?"
            self._flag_count += 1

        self.w.value["Flags"] = self._flag_count

    def _field_value(self, coordinate: tuple[int, int]) -> int:
        """
        Return the value of a certain field
        """
        row, col = coordinate

        if self._is_bomb(coordinate):
            return -1
        else:
            val = int(self._gamefield[row][col])
            return val

    def _reveal_one(self, coordinate: tuple[int, int]) -> int | None:
        """
        Reveal a single field
        """
        row, col = coordinate
        button = self._buttons[row][col]    # Pick the button corresponding to the coordinate

        # Recursion-anchor. Don't re-reveal fields that are already revealed
        if button.has_flag(CustomFlags.REVEALED):
            return None

        button.add_flags(CustomFlags.REVEALED)  # Flag it as revealed
        self._remaining_fields -= 1 # One less field remaining

        button.update(relief= "ridge", disabled = True) # Disable the button and change its style

        val = self._field_value(coordinate)
        match val:  # Let's check what we found
            case -1:    # Bomb
                button.value = "☼"
                button.update(background_color = "black", text_color_disabled = "white")
            case 0:     # Empty field
                button.update(background_color= "gray95")
                button.value = ""
                for c in self._surrounding_fields(coordinate):
                    if not self._is_bomb(c):
                        self._reveal_one(c)
            case _:     # Any other value
                button.update(background_color= "gray95")
                button.value = val
                button.update(text_color_disabled = self._colors[val - 1])  # Recolor the text according to self._colors

        return val

    def _reveal_all(self):
        """
        Reveal all fields
        """
        for r in range(self._rows):
            for c in range(self._colums):
                self._reveal_one((r,c))

    def _is_bomb(self, coordinates: tuple[int, int]) -> bool:
        """
        Check if the coordinate is in the bomb-list
        """
        return coordinates in self._bombs

    def _surrounding_fields(self, coordinate: tuple[int, int]) -> tuple[int, int]:
        """
        Return all surrounding coordinates.

        This is a generator, so it might look strange to Python-beginners.
        Check out a tutorial on Python-generators for further information
        """
        row, col = coordinate

        for r in range(
                max(row - 1, 0),
                min(self._rows, row + 2),
        ):
            for c in range(
                    max(col - 1, 0),
                    min(self._colums, col + 2),
            ):
                yield r, c  # "Return" the next value

    def _you_won(self):
        """
        Game over, you won
        """
        self._reveal_all()
        self.w.update(background_color= "lightgreen")

    def _you_lost(self):
        """
        Game over, you lost
        """
        self._reveal_all()
        self.w.update(background_color= "red")

def save_values(v: sg.ValueDict):
    """
    Save the values to the file
    """
    _save_file.update(v.to_json())

def main():
    _width = 10

    layout = [
        [
            sg.T("Rows: ", width=_width),
            sg.Slider(
                number_min=1,
                number_max=50,
                default_value=10,
                key= "Rows",
                length= 200,
            )
        ],[
            sg.T("Columns: ", width=_width),
            sg.Slider(
                number_min=1,
                number_max=75,
                default_value=10,
                key="Cols",
                expand=True
            )
        ],[
            sg.T("Bombs: ", width=_width),
            sg.Slider(
                number_min=1,
                number_max=300,
                default_value=10,
                key="Bombs",
                expand=True
            )
        ],[
            sg.Spacer(height= 10),
        ],[
            sg.Button("Start game", expand= True, key= "Start")
        ]
    ]

    w = sg.Window(
        layout,
        pady=15,
        padx=15,
        title="Minesweeper launcher"
    ).bind_destroy_event(save_values)   # When the window is closed, save_values should be called

    w.value.from_json(_save_file.to_dict()) # When the window is created, restore all file-values

    for e,v in w:
        if e == "Start":
            Minesweeper(    # Open a new popup with the specified settings
                int(v["Rows"]),
                int(v["Cols"]),
                int(v["Bombs"]),
            )

# Program-entry
if __name__ == '__main__':
    main()
