import SwiftGUI as sg

_max_characters = 50    # How many characters should be displayed maximum
_TextField_height = 5   # How many rows are shown in the text-field
_Listbox_height = 5     # How many rows the listbox has
_max_history = 30    # How many previous clipboards are saved

sg.Themes.FourColors.Emerald()  # Use a different theme, as you please

layout = [
    [
        cb := sg.Combobox(
            ["Hallo", "Welt"],
            key= "CB",
            default_event= True,
        )
    ]
]


w = sg.Window(layout, title="Clipboard history", alignment="left")
sg.clipboard_observer(w, key="ClipboardChanged", throw_initial_value=True)  # Throws an event every time the clipboard changes

print(cb.choices)

previous_clp = None # Clipboard previous loop

for e,v in w:
    print(e,v)



