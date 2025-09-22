
# SwiftGUI

A python-package to quickly create user-interfaces (GUIs).

I really liked PySimpleGUI (before they went "premium"),
but once you work a lot with it, you'll notice the downsides of it more and more.

`SwiftGUI` adapts some concepts of `PySimpleGUI`, but is even simpler (in my opinion)
and a lot less annoying to use.

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

# 28 different elements
(Version 0.8.0)

`import SwiftGUI as sg`

Call `sg.Examples.preview_all_elements()` for an overview.

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

# installation

Install using pip:
```bash
pip install SwiftGUI
```

Update to use the newest features and elements:
```bash
pip install SwiftGUI -U
```

## Why SwiftGUI instead of PySimpleGUI?
I have a lot of experience with `PySimpleGUI`, used it for years.
It is very useful, but has a lot of super annoying aspects.

Here are some improvements:
PySimpleGUI is pretty much impossible to expand, because of its messy codebase.
They also forbid the expansion of PySimpleGUI in their license.\
SwiftGUI encourages expanding the package.\
It provides various ways to create custom elements.
The simplest way is through "combined elements".

PySimpleGUI is only "simple" for smaller layouts.
There are just some things, you do in most bigger layouts, 
which are very annoying and time-consuming in PySimpleGUI.
You need to copy a lot of code and create soooooo many keys...\
SwiftGUI doesn't let you copy code directly, but makes it very easy to create and use templates.

The only ways to convey events in PySimpleGUI is breaking out of `window.read()`, or
writing events onto the tkinter-widget directly.
Due to that, in bigger layouts, the code becomes cluttered quickly and has a lot of redundancy.
Every little event occupies its own key, which made keys like `leftPart_Search_Searchbar_ClearButton` common.\
In SwiftGUI, you can throw events without defining a key.\
You can also divide the main event-loop into smaller parts, all using their own key-system.

The `sg.Table` of PySimpleGUI is the bloody worst, and I'm willing to die on that hill.
It perfectly shows everything that's wrong with PySimpleGUI.\
To modify a single row, you need to RECREATE THE WHOLE TABLE.
A performance nightmare.\
You wanna know the worst part about this?
`Tkinter`, the package behind PySimpleGUI EVEN OFFERS BUILTING METHODS TO REPLACE SINGLE ROWS!\
I was livid when I could add this functionality in 5-10 simple rows of code.\
SwiftGUIs `sg.Table` is transcendent compared to PySimpleGUI.\
There is its own tutorial where I go on ranting about PySimpleGUI's `sg.Table` for a bit longer.
Check it out.

PySimpleGUI has a lot of very small bugs.
Each one of them is not a real issue, but their sum definetly is.\
E.g.: Pressing `Ctrl`, `Shift`, or `Alt` in an `sg.Input` throws an event, even though the text wasn't changed.\
SwiftGUI doesn't tolerate these kinds of "too unimportant to care"-annoyances.

In SwiftGUI, it's a lot easier to modify/add themes.
The "global-options"-system is a lot more complex than PySimpleGUI's, 
while still being easier to use.

## Features and Differences to PySimpleGUI
(A bit redundant, I'll clean up this description soon...)

Disclaimer: I did not copy any code of PySimpleGUI.
This library is completely independent of PySimpleGUI and aims at making it obsolete.

Some of these features haven't been implemented yet, but the package is created in a way 
that all of these will be possible without any major hussle.

### Layout
The way you create layouts is pretty much the same as in PySimpleGUI.

(Not yet) However, in swiftGUI it is possible to copy parts of the layout.

### Events
In PySimpleGUI, every event has to have a key and always breaks out of `window.read()`,
slowing down the code.

In SwiftGUI, you have the option to pass "key-functions" (additionally to the normal key).
When an event occurs, these functions will be evoked too.

E.g.: Let's say you want to add a button that clears out an input-element.
In PySimpleGUI, you would need to give that button its own key, add an if-statement
to the main loop, just to make the call `window["InputKey"]("")`.

In swiftGUI, the only thing you need to do is pass a lambda-function as a key-function to
the button: `sg.Button(...,key_function=lambda w:w["InputKey"].set_value(""))`.\
Done.\
No going through the whole event-loop, no if-statements, no key "used",
not even an additional line of code.

Additionally, there are a couple of pre-made "key-functions" you can configure and use.
The clearing out of an input is one of them, so no need to write the lambda.

### Elements/Widgets
Additional to the standard-widgets of Tkinter that PySimpleGUI has,
SwiftGUI offers a selection of "combined elements" and elements with extended functionality.

These combined elements contain multiple tk-widgets that mostly get interpreted as a single value.

E.g. the `Form`-Element consists of multiple rows of text-input-combinations.
The values can either be packed into a dictionary to use less keys, 
or every `Input` gets its own key.

This is something most layouts need to have, but with PySimpleGUI, you need to create
every Element one by one, or create a wrapper (which is very janky due to PySimpleGUIs codebase).

### Expandability
SwiftGUI aims at being as easy to expand as possible.

There will be tutorials on how to use the codebase.

Feel free to take a look at `Widgets.py` and `WidgetsAdvanced.py`.

