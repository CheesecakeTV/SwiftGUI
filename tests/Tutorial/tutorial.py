import SwiftGUI as sg

my_file = sg.Files.DictFileJSON(
    "My File.json",
    defaults={
        "times_executed": 0,
    }
)

print(my_file.increment("times_executed"))

