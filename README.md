
# SwiftGUI

A python-package to quickly create user-interfaces (GUIs).

I really liked PySimpleGUI (until they went "premium"),
but once you work a lot with it, you'll notice the downsides of it more and more.

**SwiftGUI can be used almost exactly like PySimpleGUI**, but has a lot of additional features.\
Also, not gonna lie, SwiftGUI's naming is different sometimes.
`enable_event` is called `default_event`, makes more sense in my opinion.

There will be a lot of learning-material, including
- Written tutorials (see "getting started" below)
- Video tutorials (Planned for version 1.0.0)
- Application notes, which are short descriptions of actual applications
- The GitHub forum ([discussions](https://github.com/CheesecakeTV/SwiftGUI/discussions)) for questions, which you can already use

## Compatible with Python 3.10 and above
Has some minor optimizations when running in Python 3.12+.

# Getting started / documentation
[Start your journey here](https://github.com/CheesecakeTV/SwiftGUI-Docs/blob/c1d77a97ba9f07cc72434592f46abbe416d00456/01%20Basic%20tutorials/01%20Getting-started.md)

The documentation now has [its own repository](https://github.com/CheesecakeTV/SwiftGUI-Docs).

# Does your GUI look shitty?
`import SwiftGUI as sg`

Just call `sg.Themes.FourColors.Emerald()` before creating the layout.

This applies the `Emerald`-theme.

See which themes are available by calling `sg.Examples.preview_all_themes()`.

# 32 different elements, 9 different canvas-elements
(Version 0.10.0)

`import SwiftGUI as sg`

Call `sg.Examples.preview_all_elements()` for an overview of all the elements.

#  Alpha-phase!
I am already using SwiftGUI for smaller projects and personally, like it a lot so far.

However, until version 1.0.0, the package is not guaranteed to be fully downward-compatible.
Names and functions/methods might change, which could mess up your code.

For version 1.0.0, I'll sort and standardize names, so they are easier to remember.

Don't worry too much though, I already tidied up a lot.
Upcoming changes to existing code will probably be minor.

## Legal disclaimer

I did not copy any code from the (once) popular Python-package PySimpleGUI.

Even though some of the concepts are simmilar, everything was written by me or a contributor.
Element-names like `Table` and `Input` are common and not owned by PySimpleGUI.
Even if they were, they got published a long time ago under a different license.

# Installation

Install using pip:
```bash
pip install SwiftGUI
```

Update to use the newest features and elements:
```bash
pip install SwiftGUI -U
```

## Why SwiftGUI instead of PySimpleGUI?
First know that SwiftGUI can be used almost exactly like PySimpleGUI.\
You won't have to learn everything starting from 0.\
However, the naming-convention is different, but not difficult.

I have a lot of experience with `PySimpleGUI`, used it for years.\
It is very useful, and offers good compatability on a lot of platforms.

Unfortunately, at a certain level of complexity, you'll hit a wall.
All those simple features of PySimpleGUI are suddenly very messy.
I give concrete examples in the readme of the documentation.

While developing SwiftGUI, I am already using it when I'd usually use PySimpleGUI.
Let me tell you, it's sooooo much more pleasant than PySimpleGUI, even if it is still in alpha-phase.


