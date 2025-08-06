import SwiftGUI as sg

elements = [
    [0, "First row", "Second column"],
    [1, "Second row", "Second column"],
    [2, "Third row", "Second column"],
    [3, "Forth row", "Second column"],
    [4, "Fith row", "Second column"],
]

layout = [
    [
        sg.Text("Hallo Welt" * 15)
    ],
    [
        table := sg.Table(
            elements,
            headings= ("Col1", "Col2", "Col3"),
            column_width= 5,
            height = 3,
            expand= True,
        ).resize_column(1, 15)
    ]
]

w = sg.Window(layout)

for e,v in w:
    ...




