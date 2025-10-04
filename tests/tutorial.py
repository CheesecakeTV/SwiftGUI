import PIL.ImageTk

import SwiftGUI as sg
from SwiftGUI import Canvas_Elements as sgc
from pathlib import Path
import os
from PIL import Image
import tkinter as tk

#inp = Image.open("Star.png")

#outp = inp.convert("1")
#inp.save("Star.bmp")

sg.Themes.FourColors.SinCity()
# sg.Examples.preview_all_elements()
# exit()

layout = [
    [
        sg.T("Hallo Welt"),
    ],[
        my_canv := sg.Canvas(
            sgc.Line(
                (20, 10),
                (50, 10),
                width= 3,
            ),
            highlightbackground_color="red",
            key= "Canvas",
            #default_event=True,
            width= 100,
            height= 100,
            #closeenough= 5,
            confine= True,
            scrollregion= (0, 0, 200, 210)  # x1, y1, x2, y2
        ),
        sg.Scrollbar().bind_to_element(my_canv)
    ],[
        sg.Scale(
            default_event=True,
            key= "Scale",
            expand= True,
        )
    ]
]

canv_line = sg.Canvas_Elements.Line((10, 50), (10, 90), (90, 10), key="Test", color="red", color_active="green", width=3, arrowshape=(5.5, 5.5, 5.5), capstyle="round", joinstyle="miter", arrow="both")
my_canv.add_canvas_element(canv_line)
canv_line.bind_event(sg.Event.ClickLeft, key="Hello")

w = sg.Window(layout)
canv:tk.Canvas = my_canv.tk_widget

canv_line.update_coords(*(canv_line.get_coords() + ([50, 10],)))

canv_arc = sg.Canvas_Elements.Arc(
    (20, 20),
    (50, 50),
    start_angle= 45,
    extent_angle= 135,
    infill_color="red",
    width= 3,
)
my_canv.add_canvas_element(canv_arc)

canv_bitmap = sg.Canvas_Elements.Bitmap(
    (80, 80),
    "info",
    color= "yellow",
    bitmap_active="question",
)
my_canv.add_canvas_element(canv_bitmap)

canv_oval = sg.Canvas_Elements.Oval(
    (40, 40),
    (60, 60),
    width= 3,
    color = "yellow",
).attach_to_canvas(my_canv)

canv_polygon = sg.Canvas_Elements.Polygon(
    (20, 20),
    (30, 10),
    (40, 20),
    (30, 60),
    color= "lime",
    infill_color= "",
    width= 3,
).attach_to_canvas(my_canv)

canv_rectangle = sg.Canvas_Elements.Rectangle(
    *canv_line.get_boundary(),
    color= "lightblue",
    width= 3
).attach_to_canvas(my_canv)

canv_text = sg.Canvas_Elements.Text(
    (10, 90),
    "Hallo Welt",
    color = "beige",
    font_bold= True,
    fontsize= 14,
).attach_to_canvas(my_canv)

canv_image = sg.Canvas_Elements.Image(
    (80, 50),
    image= "fingerprint.png",
    image_active= "Star.png",
    image_width= 30,
).attach_to_canvas(my_canv)
# img = PIL.ImageTk.PhotoImage(Image.open("Star.png"))
# canv.create_image(30, 110, image=img, anchor="nw")


for e,v in w:
    print(e, v)
