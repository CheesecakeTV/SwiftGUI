import SwiftGUI as sg

sg.Themes.Thematic.FacebookMom()
#sg.Themes.FourColors.SinCity()
#sg.Examples.preview_all_elements(flip_readonly= True)
sg.Examples.preview_all_elements()
exit()

layout = [
    [
        my_text := sg.Text(),
    ]
]

w = sg.Window(layout, padx=30, pady=30)
my_text.value = "Awesome!"

for e, v in w:
    print(e, v)
