import SwiftGUI as sg

### Global options ###
#sg.GlobalOptions.Notebook.background_color_tabs_active = "navy"

#sg.Themes.FourColors.New()
#print(dir(sg.Themes.FourColors))
sg.Themes.FourColors.NightHorizon()
# sg.Examples.preview_all_elements()
# #sg.Examples.preview_all_themes()
#sg.Themes.FourColors.Goldfish().preview_palette()

### Layout ###
left_tab = sg.TabFrame([
    [
        sg.Listbox(
            range(10)
        ),
    ],[
        sg.MultistateButton(
            ["Hallo", "Welt", "Test", "Hühnerhof"],
            button_keys= ["H", "W", "T", "Hü"],
            default_selection= "H",
            can_deselect= False,
            key="Multistate",
            key_function= lambda val: print(val),
        )

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

w = sg.Window(layout)
#nb.value = "Harald"

### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    #print(nb.value)
    print(e,v)

### After window was closed ###
