import SwiftGUI as sg

### Global options ###
sg.Themes.FourColors.DarkGold()

### Layout ###
left_tab = sg.TabFrame([
    [
        sg.T("Text", key = "Text")
    ],[
        lb := sg.Listbox(
            range(20),
            key= "Listbox",
            default_event= True,
            key_function= sg.KeyFunctions.cycle_values("Text", "Hallo", "Welt"),
        ).set_index(0).update_scrollbar_y(cursor = "pirate"),
    ],[
        sg.Scale(background_color_active="red")
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
            default_value= 50,
            number_max= 150,
            highlightbackground_color= "red",
            label= "test",
            key = "Scale",
            default_event= True,
            tickinterval= 25,
            expand = True,
            width= 100,
            repeatdelay= 500,
            repeatinterval= 100,
            sliderlength= 50,
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
        text := sg.T("Test", padding=50)
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
    print(text.get_option("blabli"))

    if e == "Multistate":
        text.update(background_color= "red")

    #v["Listbox"] = "Funktioniert"

### After window was closed ###
