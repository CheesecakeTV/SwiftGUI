import SwiftGUI as sg
import cProfile
import pstats

def to_check():
    sg.Themes.FourColors.TransgressionTown()
    #sg.Examples.preview_all_elements()

    layout = [
        [
            sg.Button(str((i, k)), width=3) for k in range(30)
        ] for i in range(30)
    ]

    w = sg.Window(layout)

    for e,v in w:
        ...


profiler = cProfile.Profile()
profiler.enable()

to_check()

profiler.disable()

stats = pstats.Stats(profiler)
#stats.strip_dirs()
#stats.sort_stats("ncalls").print_stats(30)
#stats.sort_stats("cumtime").print_stats("_update_special_key", 30)
stats.sort_stats("tottime").print_stats(30)


