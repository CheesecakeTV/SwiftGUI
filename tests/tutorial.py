import SwiftGUI as sg

### Global options ###
#sg.GlobalOptions.Notebook.background_color_tabs_active = "navy"

#sg.Themes.FourColors.New()
#print(dir(sg.Themes.FourColors))
# sg.Themes.FourColors.NightHorizon()
# sg.Examples.preview_all_elements()
# #sg.Examples.preview_all_themes()
#sg.Themes.FourColors.Goldfish().preview_palette()

### Layout ###
left_tab = sg.TabFrame([
    [
        sg.Listbox(
            range(10)
        ),
    ]
], key= "left", fake_key= "Günther", default_event=True, key_function= lambda elem:print(elem.text))

right_tab = sg.TabFrame([
    [sg.T("Smaller element")],
    [sg.Button("Another smaller element")],
    [sg.T("<-- sg.Listbox")]
], key= "right", fake_key= "Harald")

layout:list[list[sg.BaseElement]] = [
    [
        sg.T("Test", padding=50)
    ],
    [
        nb := sg.Notebook(
            left_tab,
            right_tab,
            #default_event= True,
            key = "NB",
            #background_color_tabs_active = sg.GlobalOptions.Common_Background.background_color
        )
    ]
]

sg.GlobalOptions.Window.background_color = "red"
w = sg.Window(layout, background_color=sg.Color.orange)
nb.update(background_color = sg.Color.coral)
nb.update(background_color = None)
nb.update_to_default_value("background_color")
#nb.value = "Harald"

### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    #print(nb.value)
    print(e,v)

### After window was closed ###
