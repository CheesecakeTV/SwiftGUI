import SwiftGUI as sg
from SwiftGUI.Files import root_path

sg.Files.set_root("SwiftGUI_Template_Folder")

config_file = sg.Files.ConfigFile(
    root_path("configuration.ini"),
)

my_section = config_file.section(
    name= "Example section",
    defaults= {
        # Add your default values here
    },
)


