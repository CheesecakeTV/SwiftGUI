import SwiftGUI as sg
from PIL import Image # pip install pillow
from pathlib import Path    # pip install pathlib   (Should be builtin though...)
import tempfile as temp
import os

my_theme = sg.Themes.FourColors.DarkGold
my_theme()

def img_to_ico(img_path: str, output_folder: Path, force_size: tuple[int, int] = None):
    """
    Convert an image of various types to .ico
    :param force_size: Pass values to convert the ico to said size
    :param img_path:
    :param output_folder:
    :return:
    """
    img_path = Path(img_path)
    ico_path = output_folder / (img_path.stem + ".ico")

    img = Image.open(img_path)

    if force_size:
        img.resize(force_size)

    img.save(ico_path, format = "ICO")

layout = [
    [
        sg.FileBrowseButton(
            "Choose file(s)",
            file_browse_type="open_multiple",
            key = "FileBrowse",
            #key_function = lambda elem: w["Convert"].update(background_color = sg.Color.PaleGreen1 if elem.value else sg.Color.coral).set_value(f"Convert ({len(elem.value)})"),
            key_function = lambda elem: w["Convert"].set_value(f"Convert ({len(elem.value)})"),
            dont_change_on_abort= True,
            file_browse_filetypes= (
                ("Image/graphic", (
                    # All formats supported by pillow
                    ".png",
                    ".jpeg",
                    ".jpg",
                    ".avif",
                    ".blp",
                    ".bmp",
                    ".dds",
                    ".dib",
                    ".eps",
                    ".gif",
                    ".icns",
                    ".ico",
                    "im",
                    ".jpeg 2000",
                    ".mpo",
                    ".msp",
                    ".pcx",
                    ".pfm",
                    ".ppm",
                    ".qoi",
                    ".sgi",
                    ".spider",
                    ".tga",
                    ".tiff",
                    ".webp",
                    ".xbm",

                    # Read-only-formats
                    ".cur",
                    ".dcx",
                    ".fits",
                    ".fli",
                    ".flc",
                    ".fpx",
                    ".ftex",
                    ".gbr",
                    ".gd",
                    ".imt",
                    ".iptc",
                    ".naa",
                    ".mcidas",
                    ".mic",
                    ".pcd",
                    ".pixar",
                    ".psd",
                    ".sun",
                    ".wal",
                    ".wmf",
                    ".emf",
                    ".xpm",
                )),
            ),
        )
    ],[
        sg.Form(
            (
                ("Force Height", "Height"),
                ("Force Width", "Width"),
            ),
            key = "ForceSize",
            default_values= (30, 30),
        )
    ],[
        sg.Button(
            "Convert (0)",
            key="Convert",
        )
    ]
]

_tempfolder_raw = temp.TemporaryDirectory()
_tempfolder = Path(_tempfolder_raw.name)

w = sg.Window(layout, title="Image to icon converter")

for e,v in w:
    #print(e,v)

    if e == "Convert":
        fs_x = w["ForceSize"].value.get("Width")
        fs_y = w["ForceSize"].value.get("Height")
        fs = None
        if fs_x and fs_y:
            try:
                fs = (int(fs_x), int(fs_y))
            except ValueError:
                pass

        if not w["FileBrowse"].value:
            continue

        for name in w["FileBrowse"].value:
            img_to_ico(name, _tempfolder, force_size= fs)
            os.system("start " + _tempfolder_raw.name)

