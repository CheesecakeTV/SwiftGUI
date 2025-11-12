import SwiftGUI as sg
import time

sg.Examples.preview_all_elements()
exit()

@sg.call_periodically(1, counter_reset= 0)
def test(count):
    print(count)

sg.Popups.show_text("Test")
time.sleep(3)

layout = [
    [
        sg.T("Test")
    ]
]

w = sg.Window(layout, padx=30, pady=30)

for e, v in w:
    print(e, v)

