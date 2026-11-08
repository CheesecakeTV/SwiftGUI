
# SwiftGUI
A python-package to easily create user-interfaces (GUIs).

While most packages focus either on small, or big applications, SwiftGUI does both.

## Compatible with Python 3.10 and above
Has some minor optimizations when running in Python 3.12+.

# Getting started / documentation
[Start your journey here](https://github.com/CheesecakeTV/SwiftGUI-Docs/blob/main/01%20Basic%20tutorials/01%20Getting-started.md)

[Documentation](https://github.com/CheesecakeTV/SwiftGUI-Docs).

# Vibe-coding free
No AI was used in writing this code.

The only way I used it was to research really specific topics with tkinter.

Even the documentation was written completely AI-free.
Takes me around 2 hours per document, but that's a good price for keeping everything slop-free.

Yes, this does slow down development quite a bit, but I trust myself to be more reliable than an AI agent.

# 38 different elements, 9 different canvas-elements
(Version 0.12.0)

`import SwiftGUI as sg`

Call `sg.Examples.preview_all_elements()` for an overview of all currently available elements.

# Does your GUI look bad?
`import SwiftGUI as sg`

Just call `sg.Themes.FourColors.Emerald()` before creating the layout.

This applies the `Emerald`-theme, my personal favorite.

See which themes are available by calling `sg.Examples.preview_all_themes()`.

#  Final minor version before Beta starts!
You might have noticed that updates for SwiftGUI are rarer than they used to be.
That's actually a good sign, it means I find less things to add/correct.

There will not be version 0.13.0, but 1.0.0 instead.

I do have a couple of major tasks on my list before rolling out 1.0 though.
Fixing the treeview for example.

# Installation
Install using pip:
```bash
pip install SwiftGUI
```

Regularely update SwiftGUI for the newest features and bugfixes:
```bash
pip install SwiftGUI -U
```

# NOT a clone of PySimpleGUI
SwiftGUI is it's own package, with its own functionality.

I really liked PySimpleGUI (until they went "premium"),
but once you work a lot with it, you'll notice its downsides more and more.

The basics of SwiftGUI are almost the same as PySimpleGUI.
So if you know PySimpleGUI, you already know many concepts of SwiftGUI.

There is already a collection of helpful learning material, including:
- Written tutorials (see "getting started" above)
- Application notes, which summarize different tutorials regarding specific applications
- Examples, which show an actual application of SwiftGUI
- The GitHub forum ([discussions](https://github.com/CheesecakeTV/SwiftGUI/discussions)) for questions

Video tutorials are planned for version 1.0.0.

## Why SwiftGUI instead of PySimpleGUI?
I have a lot of experience with `PySimpleGUI`, used it for years.\
It is very useful for smaller applications.

Unfortunately, at a certain level of complexity, you'll hit a wall.\
All those simple features that make PySimpleGUI great, are suddenly very annoying.

In the earlier versions of SwiftGUI, it was ment to "fix" annoying things in PySimpleGUI.
For example:
- You are forced to use the event-loop for every tiny functionality
- You can pretty much forget about editing elements, since they are implemented so convoluded
- Some elements throw events wrong, including sg.Table and sg.Input

Nowadays, SwiftGUI's functionality goes far beyond what PySimpleGUI has to offer.

The reason is simple:
SwiftGUI is built for modularity and expandability.
You can easily create templates, themes, custom popups, modify elements, etc.

Also, SwiftGUI works a lot better with multiple windows.
Creating a second window is almost as simple as creating a single one.

A lot more features are described/mentioned in the documentation.
