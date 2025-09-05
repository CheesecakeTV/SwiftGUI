from SwiftGUI.Compat import batched
import SwiftGUI as sg

def _get_single_preview(theme: type, name: str) -> sg.Frame:
    sg.GlobalOptions.reset_all_options()
    theme()  # Apply theme
    sg.GlobalOptions.Common_Textual.fontsize = 8
    sg.GlobalOptions.Button.fontsize = 8

    return sg.Frame([
        [
            sg.T("Theme: "),
            sg.T(f"{name}").bind_event(sg.Event.ClickLeft, key_function= lambda val: print(val)),
        ],[
            sg.HSep()
        ],[
            sg.Input("Hello!"),
        ],[
            sg.Input("Hello, I'm readonly!",readonly=True),
        ],[
            sg.HSep()
        ], [
            sg.LabelFrame([
                [
                    sg.Check("I like it!"),
                    sg.Button("Take a closer look", key = name),
                ], [
                    sg.Listbox(["Listbox", "with", "some", "elements", "and", "a scrollbar"], width=15, height=3, scrollbar=True),
                    sg.VSep(),
                    sg.TextField("TextField", width=15, height=3, scrollbar=False)
                ]
            ], text= "LabelFrame")
        ]
    ], apply_parent_background_color= False)

def preview_all_themes(max_rows: int = 4, max_cols: int = 5) -> None:
    """
    Have a look at all possible (prebuilt) themes
    :return:
    """
    layout = list()
    grouped = dict()

    # Group all themes by their suffix
    for key, theme in sorted(list(sg.Themes.all_themes.items())):
        suffix = theme.suffix

        if key.startswith("_"):
            continue

        if suffix not in grouped:
            grouped[suffix] = list()

        grouped[suffix].append(_get_single_preview(theme, key))

        #layout.append(_get_single_preview(theme, key))

    # "Cut" the groups into smaller groups so they fit in the layout
    grouped_and_cut = dict()
    for suffix, group in grouped.items():
        group = list(batched(group, max_cols))

        if len(group) <= max_rows:  # No cutting needed
            grouped_and_cut[suffix] = group
            continue

        group_groups = batched(group, max_rows)
        for n, g in enumerate(group_groups):
            grouped_and_cut[f"{suffix} ({n})"] = g

    #layout = batched(layout, 7)
    tab_frames = list()
    for key, group in grouped_and_cut.items():
        tab_frames.append(sg.TabFrame(
            group,
            fake_key= key
        ))

    sg.GlobalOptions.reset_all_options()
    sg.Themes.FourColors.HotAsh()
    layout = [
         [
             sg.T("Click on the title of any theme and it will be printed to the console", fontsize= 14, expand= True)
         ],[
            sg.Notebook(*tab_frames)
        ]
    ]

    w = sg.Window(layout, title="Preview of all elements", alignment="left")

    for e,v in w:
        sg.GlobalOptions.reset_all_options()
        sg.Themes.all_themes[e]()
        sg.Examples.preview_all_elements(include_images= False)

