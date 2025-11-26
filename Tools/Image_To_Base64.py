import base64
import io

import SwiftGUI as sg
from PIL import Image # pip install pillow
from pathlib import Path    # pip install pathlib   (Should be builtin though...)

my_theme = sg.Themes.FourColors.TransgressionTown
my_theme()

def img_to_b64(img_path: str, force_size: tuple[int, int] = None) -> bytes:
    """
    Convert an image of various types to .ico
    :param force_size: Pass values to convert the ico to said size
    :param img_path:
    :return:
    """
    img_path = Path(img_path)

    buf = io.BytesIO()
    img = Image.open(img_path)

    if force_size:
        img = img.resize(force_size)

    img.save(buf, format= "png")

    return base64.b64encode(buf.getvalue())

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
        )
    ],[
        sg.Button(
            "Convert (0)",
            key="Convert",
        )
    ],[
        textfield := sg.TextField(
            height= 10,
            width= 100,
            wrap= "none",
            readonly= True,
        )
    ],[
        sg.Button(
            "Copy to clipboard",
            key_function= lambda :sg.clipboard_copy(textfield.value)
        )
    ]
]

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

        ml_value = ""
        if not w["FileBrowse"].value:
            textfield.value = "Error, no file(s) selected"
            continue

        for name in w["FileBrowse"].value:
            ml_value += f"{Path(name).stem.replace(' ','_')}: bytes = {img_to_b64(name, force_size=fs)}\n"

        textfield.value = ml_value
        print(ml_value)
        print()

