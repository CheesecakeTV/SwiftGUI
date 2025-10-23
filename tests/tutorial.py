import SwiftGUI as sg
import numpy as np

sg.Themes.FourColors.SinCity()

layout = [
    [
        my_plot := sg.Matplot(navigation_bar=True)
    ]
]

x = np.linspace(-20, 20, 100)
y = np.sin(x) / x

my_plot.plot(x, y)

w = sg.Window(layout, padx=30, pady=30)

for e,v in w:
    ...

