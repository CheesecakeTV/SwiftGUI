import SwiftGUI as sg


def preview_all_elements():
    sg.GlobalOptions.TabFrame.alignment = "left"
    #sg.GlobalOptions.SeparatorHorizontal.color = sg.Color.navy

    smaller_widgets = sg.TabFrame([
        [
            sg.T("sg.Text / sg.T")
        ],[
            sg.HSep()
        ],[
            sg.Button("sg.Button")
        ],[
            sg.HSep()
        ],[
            sg.Checkbox("sg.Checkbox"),
        ],[
            sg.Checkbox("Also sg.Checkbox\nbut check_type='button'", check_type= "button"),
        ],[
            sg.HSep()
        ],[
            sg.Input("sg.Input / sg.In")
        ],[
            sg.HSep()
        ],[
            sg.Radiobutton("sg.Radiobutton", group= "a"),
            sg.Radiobutton("or sg.Radio", group= "a")
        ],[
            sg.HSep()
        ],[
            sg.Spinbox(5, number_max= 100, number_min= -100),
            sg.T("<-- sg.Spinbox / sg.Spin")
        ],[
            sg.HSep()
        ],[
            sg.T("Do you believe in ghosts?"),
        ],[
            sg.T("If so, there is an invisible sg.Spacer"),
            sg.Spacer(width=50)
        ],[
            sg.HSep()
        ],[
            sg.T("These lines between different element-types\n"
                 "are sg.HorizontalSeparator, or sg.HSep."),
            sg.VSep(),
            sg.T("sg.VerticalSeparator,\n"
                 "or sg.VSep\n"
                 "<-- looks like this")
        ]
    ], fake_key= "Small elements")

    extended_elements = sg.TabFrame([
        [
            sg.ColorChooserButton("sg.ColorChooserButton"),
        ],[
            sg.HSep(),
            sg.Spacer(height = 10),
        ],[
            sg.T("sg.FileBrowseButton (different file_browse_type)")
        ],[
            sg.FileBrowseButton("open_single", file_browse_type="open_single"),
            sg.FileBrowseButton("save_single", file_browse_type="save_single"),
            sg.FileBrowseButton("open_multiple", file_browse_type="open_multiple"),
            sg.FileBrowseButton("open_directory", file_browse_type="open_directory"),
        ]
    ], fake_key= "Extended elements")

    containers = sg.TabFrame([
        [
            sg.Frame([
                [sg.T("sg.Frame")],
                [sg.T("It is here, but you probably can't see it...")]
            ], alignment="left")
        ],[
            sg.Spacer(height=30)
        ],[
            sg.LabelFrame([
                [sg.T("sg.LabelFrame")],
                [sg.T("Has a nice border and a label")]
            ], text= "sg.LabelFrame", alignment= "left")
        ],[
            sg.Spacer(height=30)
        ],[
            sg.TabFrame([
                [sg.T("sg.TabFrame")],
                [sg.T("Looks like a normal frame,")],
                [sg.T("What did you expect?")],
                [sg.T("Useful in combination with sg.Notebook though.")]
            ], alignment="left", fake_key= "A")
        ],[
            sg.Spacer(height=20)
        ],[
            sg.Notebook(
                sg.TabFrame([[sg.T("sg.Notebook")]], fake_key="Tab1"),
                sg.TabFrame([[sg.T("still sg.Notebook")]], fake_key="Tab2"),
            )
        ]
    ], fake_key= "containers")

    images = sg.TabFrame([
        [
            sg.T("sg.Image:"),
        ],[
            sg.Image(sg.file_from_b64(sg.python_logo), width= 200),
            sg.Image(sg.file_from_b64(sg.python_logo), width= 150),
            sg.Image(sg.file_from_b64(sg.python_logo), width=100),
        ],[
            sg.HSep()
        ],[
            sg.T("sg.ImageButton")
        ],[
            sg.ImageButton(sg.file_from_b64(sg.python_logo), height=150),
            sg.T("(The image has a strange format)")
        ]
    ], fake_key = "images")

    bigger_elements = sg.TabFrame([
        [
            sg.Listbox(["sg.Listbox","simple way to","create lists"], width= 50, key= "List")
        ],[
            sg.Spacer(height= 50)
        ],[
            sg.Table(
                [
                    ["sg.Table", "Some row", 5],
                    ["Very cool element", "Some other row", 2],
                ], headings = ("A column", "Another one", "Number"), column_width= 15,
            )
        ],[
            sg.Spacer(height = 30),
        ],[
            sg.TextField("sg.TextField\n\nA big field for text", width= 50, height=5)
        ]
    ], fake_key= "Big elements")

    layout = [
        [
            sg.T("If this looks a bit shitty, try applying a theme.\n"
                 "This example is used to test themes,\n"
                 "so it's not supposed to look good without it.")
        ],[
            sg.Spacer(height=10)
        ],[
            sg.Notebook(
                smaller_widgets,
                extended_elements,
                containers,
                images,
                bigger_elements,
            )
        ]
    ]

    w = sg.Window(layout, title= "Preview of all currently available elements")
    w["List"].index = 2

    for e,v in w:
        ...

