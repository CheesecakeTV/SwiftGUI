
# SwiftGUI

A python-package to easily create user-interfaces (GUIs).

While most packages focus either on small, or big applications, SwiftGUI does both.

## Compatible with Python 3.10 and above
Has some minor optimizations when running in Python 3.12+.

# Getting started / documentation
[Start your journey here](https://github.com/CheesecakeTV/SwiftGUI-Docs/blob/main/01%20Basic%20tutorials/01%20Getting-started.md)

The documentation now has [its own repository](https://github.com/CheesecakeTV/SwiftGUI-Docs).

# Completely vibe-coding free
No AI was used in writing this code.

The only way I used it was to research really specific topics with tkinter.

I did not use AI to write, check, correct, or refractor code.

Even the documentation was written completely AI-free.
Takes me around 2 hours per document, but that's a good price for keeping everything slop-free.

# 35 different elements, 9 different canvas-elements
(Version 0.11.0)

`import SwiftGUI as sg`

Call `sg.Examples.preview_all_elements()` for an overview of all currently available elements.

# Does your GUI look bad?
`import SwiftGUI as sg`

Just call `sg.Themes.FourColors.Emerald()` before creating the layout.

This applies the `Emerald`-theme, my personal favorite.

See which themes are available by calling `sg.Examples.preview_all_themes()`.

#  Alpha-phase!
I am already using SwiftGUI for smaller projects and personally, like it a lot so far.

However, until version 1.0.0, downward-compatability is not a priority.
Names and functions/methods might change, which could potentially mess up your code.

For version 1.0.0, I'll sort and standardize names, so they are easier to remember.
After version 1.0.0, there will be little to no changes that might break existing code.
If changes can't be avoided, there will be a separate changelog which shows everything you need to
adjust so you may update without issues.

Don't worry too much though, the package is pretty much ready for beta-phase.

# Installation
Install using pip:
```bash
pip install SwiftGUI
```

Update SwiftGUI for the newest features and elements:
```bash
pip install SwiftGUI -U
```

# NOT a clone of PySimpleGUI
SwiftGUI is it's own package with its own functionality.

I really liked PySimpleGUI (until they went "premium"),
but once you work a lot with it, you'll notice the downsides of it more and more.

**SwiftGUI can be used very simmilar to PySimpleGUI**, but has a lot of additional features.\
So if you know PySimpleGUI, you won't need to start from scratch.

Also, there will be a lot of learning-material, including
- Written tutorials (see "getting started" below)
- Video tutorials (Planned for version 1.0.0)
- Application notes, which are short descriptions of actual applications
- Examples, which show an actual application of SwiftGUI
- The GitHub forum ([discussions](https://github.com/CheesecakeTV/SwiftGUI/discussions)) for questions

## Why SwiftGUI instead of PySimpleGUI?
I have a lot of experience with `PySimpleGUI`, used it for years.\
It is very useful for smaller applications.

Unfortunately, at a certain level of complexity, you'll hit a wall.\
All those simple features that make PySimpleGUI great, are suddenly very annoying.

What annoys me the most is that PySimpleGUI forces you to use only the event-loop for functionality.
That means, every tiny tiniest functionality needs a key and code in the event-loop.

SwiftGUI on the other hand offers many different ways to connect layout with functionality.
That makes it easy to "copy and paste" parts of the layout.

SwiftGUI also supports multiple windows much better, with every window having its own event-loop.

On top of that, SwiftGUI enables expandability everywhere.
You can easily create your own elements, themes, popups and templates.

