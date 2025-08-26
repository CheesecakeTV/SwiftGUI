import SwiftGUI as sg

### Global options ###
sg.Themes.FourColors.Emerald()
sg.Examples.preview_all_elements()
exit()

### Layout ###
left_tab = sg.TabFrame([
    [
        sg.Listbox(
            range(10),
            key= "Listbox",
            default_event= True,
        ).set_index(0),
    ],[
        sg.MultistateButton(
            ["Hallo", "Welt", "Test"],
            button_keys= ["H", "W", "T", "Hü"],
            default_selection= "H",
            can_deselect= False,
            key="Multistate",
            key_function= lambda val: print(val),
        )
    ],[
        sg.Scale(
            default_value= 50.5,
            highlightbackground_color= "red",
            label= "test",
            key = "Scale",
            default_event= True,
            digits= 2,
            resolution= 0.1,
        )
    ]
], key= "left", default_event=True, key_function= lambda elem:print(elem.text))

right_tab = sg.TabFrame([
    [sg.T("Smaller element")],
    [sg.Button("Another smaller element", key= "Button")],
    [sg.T("<-- sg.Listbox")]
], key= "right")

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
            default_event= True,
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

    #v["Listbox"] = "Funktioniert"

### After window was closed ###
