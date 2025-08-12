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
        sg.Frame([[table := sg.Table(
            elements * 10,
            headings= ("Col1", "Col2", "Col3"),
            height = 3,
        )]]),
        sg.TextField("Big TextField", height=10, width=10),
    ]
]

w = sg.Window(layout)

for e,v in w:
    ...




