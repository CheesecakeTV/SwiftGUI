import SwiftGUI as sg

# Init the file
main_config = sg.Files.ConfigFile("Config.ini")

general_section = main_config.section("General", defaults={
    "four_colors_theme": "Emerald",
    "title": "SwiftGUI example",
})

layout_section = main_config.section("Layout", defaults={
    "font_size": 12,    # Will be converted to string automatically
    "submit_button": True,
}, json_defaults={
    "form_texts": [
        "Name",
        "Age",
        "Occupation",
    ]
})

theme = getattr(sg.Themes.FourColors, general_section["four_colors_theme"])
theme() # Apply the theme

sg.GlobalOptions.Common_Textual.fontsize = layout_section.get_int("font_size")
sg.GlobalOptions.Button.fontsize = None # Remove the overwritten value

layout = [
    [
        sg.T("Please enter your information:"),
    ], [
        sg.Form(
            layout_section.get_json("form_texts"),
        )
    ]
]

if layout_section.get_bool("submit_button"):
    layout.append([
        sg.Button("Submit")
    ])

w = sg.Window(layout, title= general_section["title"])

for e,v in w:
    ...

