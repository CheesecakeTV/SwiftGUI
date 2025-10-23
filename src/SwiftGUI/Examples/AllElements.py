import SwiftGUI as sg
import SwiftGUI.Canvas_Elements as sgc

python_logo: bytes = b'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'

def preview_all_elements():
    sg.GlobalOptions.TabFrame.alignment = "left"
    #sg.GlobalOptions.SeparatorHorizontal.color = sg.Color.navy

    group = sg.RadioGroup()

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
            sg.Checkbox("Also sg.Checkbox\nbut check_type='button'", check_type= "button"),
        ],[
            sg.HSep()
        ],[
            sg.Combobox(["sg.Combobox", "sg.Combo"])
        ],[
            sg.HSep()
        ],[
            sg.Scale(label= "sg.Scale", expand= True)
        ],[
            sg.HSep()
        ],[
            sg.Input("sg.Input / sg.In")
        ],[
            sg.HSep()
        ],[
            sg.Radiobutton("sg.Radiobutton", group= group),
            sg.Radiobutton("or sg.Radio", group= group)
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
        ],[
            sg.HSep(),
        ],[
            sg.T("sg.Progressbar:"),
            sg.Progressbar(expand= True).start(0.09),
            sg.VSep(),
            sg.T("sg.ProgressbarVertical:"),
            sg.ProgressbarVertical().start(),
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
        ], [
            sg.GridFrame([
                [
                    sg.T("sg.Gridframe", padding=5),
                    sg.VSep(padding=0),
                ],[
                    sg.HSep(),
                    sg.T(),
                    sg.HSep(),
                ],[
                    sg.T(),
                    sg.VSep(padding=0),
                    sg.T("Arrange things in a grid", padding=5)
                ],[
                    sg.HSep(),
                    sg.T(),
                    sg.HSep(),
                ],[
                    sg.T("Cool, isn't it?", padding=5),
                    sg.VSep(padding=0)
                ]
            ])
        ], [
            sg.Spacer(height=20)
        ],[
            sg.Notebook(
                sg.TabFrame([[sg.T("sg.Notebook")]], fake_key="Tab1"),
                sg.TabFrame([[sg.T("still sg.Notebook")]], fake_key="Tab2"),
            )
        ],[
            sg.Spacer(height=20)
        ],[
            sg.SubLayout(sg.Frame([
                [
                    sg.T("sg.SubLayout"),
                ],[
                    sg.T("A seperate layout inside your layout.")
                ],[
                    sg.T("It has seperate keys and its own segregated event-loop.")
                ]
            ], alignment="left"))
        ]
    ], fake_key= "containers")

    images = sg.TabFrame([
        [
            sg.T("sg.Image:"),
        ],[
            sg.Image(sg.file_from_b64(python_logo), image_width= 200),
            sg.Image(sg.file_from_b64(python_logo), image_width= 150),
            sg.Image(sg.file_from_b64(python_logo), image_width=100),
        ],[
            sg.HSep()
        ],[
            sg.T("sg.ImageButton")
        ],[
            sg.ImageButton(sg.file_from_b64(python_logo), image_height=150),
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

    combined_elements = sg.TabFrame([
        [
            sg.Form(
                ["sg.Form", "useful for", "creating forms"],
                big_clear_button= True,
                submit_button= True,
                default_values= ("", "", "Click on Clear"),
            )
        ],[
            sg.HSep()
        ],[
            sg.MultistateButton(
                [
                    "sg.Multistate",
                    "Works like sg.Radio",
                    "But looks cooler",
                ],
                default_select_first= True,
                horizontal_orientation= True,
                key_function= lambda val:console.print(val),
            )
        ],[
            sg.HSep()
        ], [
            sg.T("sg.Console:")
        ], [
            console := sg.Console(

            ).update_after_window_creation(
                width= 40,
                height= 8
            )
        ]
    ], fake_key= "Combined elements")

    canvas_tab = sg.TabFrame([
        [
            sg.T("sg.Canvas"),
        ],[
            sg.T("(import SwiftGUI.Canvas_Elements as sgc)")
        ],[
            sg.GridFrame([
                [
                    canv := sg.Canvas(  # The indentation is great, I know :D
                        sgc.Text((10, 15), "sgc.Arc:"),
                        sgc.Arc((80, 10), (95, 25), width=2, extent_angle= 120),
                        sgc.Arc((100, 10), (115, 25), width=2, extent_angle=120, style= "arc"),
                        sgc.Arc((120, 10), (135, 25), width=2, extent_angle=120, style= "chord"),

                        sgc.Text((10, 45), "sgc.Bitmap:"),
                        sgc.Bitmap((115, 45),  "hourglass"),
                        sgc.Bitmap((135, 45), "warning"),
                        sgc.Bitmap((155, 45), "questhead"),

                        sgc.Text((10, 75), "sgc.Line:"),
                        sgc.Line((100, 75), (110, 85), width= 2),
                        sgc.Line((115, 75), (125, 85), (125, 75), (135, 75), smooth=True, width= 2),
                        sgc.Line((140, 75), (170, 85), width=2, arrow="both"),

                        sgc.Text((10, 105), "sgc.Oval:"),
                        sgc.Oval((100, 95), (120, 115), width= 2, dash= (5,5)),
                        sgc.Oval((130, 95), (140, 115), width=2),

                        sgc.Text((10, 135), "sgc.Polygon:"),
                        sgc.Polygon((130, 125), (140, 135), (135, 145)),
                        sgc.Polygon((140, 120), (160, 140), (180, 140), (160, 120), width= 3, joinstyle= "round", infill_color= ""),

                        sgc.Text((10, 165), "sgc.Rectangle:"),
                        sgc.Rectangle((130, 155), (150, 175), width= 5),
                        sgc.Rectangle((160, 155), (190, 175), width=2, dash=(11, 1)),

                        sgc.Text((10, 195), "sgc.Text:"),
                        sgc.Text((90, 195), "Example", fonttype= sg.font_windows.Comic_Sans_MS, font_underline= True, font_bold= True),

                        sgc.Text((10, 225), "sgc.Image:"),
                        sgc.Image((100, 225), sg.file_from_b64(python_logo), anchor= "w", image_width= 15),

                        sgc.Element(
                            (10, 245),
                            sg.Frame([
                                [
                                    sg.T("sgc.Element")
                                ],[
                                    sg.Button("Put any sg-element onto your canvas!!")
                                ]
                            ]),
                            anchor= "nw",
                        ),

                        sgc.Text(
                            (295, 100),
                            "sg.Scrollbar ->",
                            anchor= "e"
                        ),
                        sgc.Text(
                            (150, 325),
                            "↓ sg.ScrollbarHorizontal ↓",
                            anchor= "s"
                        ),

                        height= 330,
                        width= 300,
                        confine= True,
                        scrollregion= (0, 0, 500, 500),
                    ),
                    sg.Scrollbar().bind_to_element(canv)
                ],[
                    sg.ScrollbarHorizontal().bind_to_element(canv)
                ]
            ])
        ]
    ], fake_key= "Canvas")

    try:
        import SwiftGUI_Matplot
        swiftgui_matplotlib = [
            [
                my_plot := SwiftGUI_Matplot.Matplot(
                    title= "SwiftGUI_Matplot.Matplot"
                )
            ]
        ]
        x = list(range(-11, 12))
        y = [(i / 3) ** 3 for i in x]
        my_plot.plot(x, y)
    except ImportError:
        swiftgui_matplotlib = [
            [
                sg.T("Module not found!"),
            ],[
                sg.T("Install "),
                sg.In("SwiftGUI_Matplot", readonly= True, takefocus=False, justify="center"),
                sg.T(" to use this feature")
            ]
        ]

    swiftgui_matplot = sg.TabFrame(swiftgui_matplotlib, text= "Matplot", pady=30)

    tabs = [
        smaller_widgets,
        extended_elements,
        containers,
        bigger_elements,
        combined_elements,
        images,
        canvas_tab,
        swiftgui_matplot,
    ]

    layout = [
        [
            sg.T("If this looks bad, try applying a theme.\n"
                 "Just call sg.Themes.FourColors.Emerald()\n"
                 "before starting this example.")
        ],[
            sg.Spacer(height=10)
        ],[
            sg.Notebook(
                *tabs,
            )
        ]
    ]

    w = sg.SubWindow(layout, title="Preview of all currently available elements")
    w["List"].index = 2

    #w.block_others_until_close()
    w.loop()

