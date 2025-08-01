
# Getting started
[Start your journey here](https://github.com/CheesecakeTV/SwiftGUI/wiki/Getting-started#getting-started)

# Still WIP
But growing quickly. Give it 1-2 month and you will use it for every GUI you create.

# SwiftGUI

A python-package to quickly create user-interfaces (GUIs).

I really liked PySimpleGUI (before they went "premium"), 
but their codebase is an utter mess.

`SwiftGUI` adapts some concepts of `PySimpleGUI`, but is even simpler (in my opinion)
and allows writing less offputting code.

## Legal disclaimer

I did not copy any code from the (once) popular Python-package PySimpleGUI.

Even though some of the concepts are simmilar, everything was written bei me or a contributor.
Element-names like `Table` and `Input` are common and not owned by PySimpleGUI.
Even if they were, they got published a long time ago under a different license.

# installation

Install using pip:
```bash
pip install SwiftGUI
```

## Why SwiftGUI?
I have a lot of experience with `PySimpleGUI`, used it for years.
It is very useful, but has a lot of super annoying aspects.

This is what I hate about it:
- PySimpleGUI is pretty much impossible to expand, because of the codebase.
- PySimpleGUI is only efficient for smaller layouts.
There are just some things, you do in most bigger layouts, 
which are very annoying and time-consuming.
- PySimpleGUI doesn't really let you copy parts of your layout automatically.
If you want to copy it, you must copy code (or create a custom function).
When you want to change certain aspects of all copied elements, 
you need to change it in every copy. Very inefficient.
- The only ways to convey events in PySimpleGUI is through breaking out of `window.read()`, or
writing events onto the tkinter-widget directly.
Due to that, in bigger layouts, the code becomes cluttered quickly and has a lot of redundancy.

`SwiftGUI` is the answer to these negative aspects.
It allows you to create bigger GUIs, quickly and elegantly.

## Features and Differences to PySimpleGUI
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
to the main loop, just to make the call `window["InputKey"]("")"`.

In swiftGUI, the only thing you need to do is pass a lambda-function as a key-function to
the button: `sg.Button(...,key_function=lambda w:w["InputKey"].set_value(""))`.\
Done.\
No breaking out of window.loop(), no if-statement, no key "used",
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

