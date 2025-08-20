import SwiftGUI as sg

### Global options ###
sg.GlobalOptions.Common_Textual.fontsize = 14
SG_01: bytes = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAbklEQVR4nGNgGGjACCJs56X/J0fz4aSZjCwwzq9v7CRpZuP6CaZZkAU1LMtQFN043oVXHMMAYjUhAyasong0oAMWdAFkm9ENgckhizOh2wrDxLqKCZftxAIWdAFchuASZyHkRHziKAawQRPGCAQAhZAq+up6rqwAAAAASUVORK5CYII='

### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.Text("Hi Welt")
    ],[
        sg.Text("Another test")
    ],[
        sg.ImageButton(sg.file_from_b64(SG_01), height=60, background_color_active=sg.Color.orange)
    ],[
        #sg.Image("Mond.gif")
    ]
]

w = sg.Window(layout, icon = sg.file_from_b64(SG_01))


### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    ...

### After window was closed ###
