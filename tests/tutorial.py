import SwiftGUI as sg

sg.Themes.FourColors.HotAsh()
sg.Examples.preview_all_elements()
exit()

tab1 = sg.Frame([
    [
        sg.T("This is Tab 1!")
    ],[
        sg.Button("Some elements")
    ],[
        sg.Listbox(range(10)).set_index(3)
    ]
], key= "Tab 1")

tab2 = sg.Frame([
    [
        sg.T("This is Tab 2!")
    ],[
        sg.Button("Some elements")
    ]
], key= "Tab 2")

tab3 = sg.Frame([
    [
        sg.T("This is Tab 3!")
    ],[
        sg.Button("Some elements")
    ]
], key= "Tab 3")

layout = [
    [
        my_nb := sg.Notebook(
            tab1, tab2, tab3,
            default_event= True,
            key_function= lambda: print("Tab changed!"),
        )
    ]
]

w = sg.Window(layout, padx=30, pady=30)

for e,v in w:
    print(e, v)

