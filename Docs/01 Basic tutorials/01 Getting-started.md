
# Getting started

This tutorial will help you create easy and very useful interfaces.

If you haven't already, install SwiftGUI using pip:
```bash
pip install swiftGUI
```

You'll notice, that your GUIs might look quite different to the screenshots in these tutorials.
I'm writing these tutorials parallel to programming new features.
The visuals improved a lot after writing some of the earlier tutorials.

Functionally, the tutorials will stay up to date, I promise!

This library is simmilar to PySimpleGUI, but has a lot of different/additional features.
If you already know PySimpleGUI, this tutorial will be very easy.

# Basic template

For every GUI, you should use this template, until you are familiar with the basic functionality:
```py
import SwiftGUI as sg
from SwiftGUI import Color

### Global options ###


### Layout ###
layout:list[list[sg.BaseElement]] = [
    
]

w = sg.Window(layout)

### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    ...

### After window was closed ###

```
You can always find that template here: [`Examples/Beginner-friendly/_template.py`](https://github.com/CheesecakeTV/SwiftGUI/blob/c23cdca4618a702af09bb4391a5e798ee12aaf59/Examples/Beginner-friendly/_template.py) (GitHub-Repo).

# Layout
The layout contains all elements to be shown inside the GUI.
As you might see, the typehint expects a "double-list", or lists inside a list.

Every "inner" list represents a row of elements.

E.g. two text-elements inside the same row:
```py
layout:list[list[sg.BaseElement]] = [
    [
        sg.Text("Hello"),
        sg.Text("World")
    ]
]
```
![](../assets/images/2025-08-05-13-24-19.png)


Two text-elements in different rows:
```py
layout:list[list[sg.BaseElement]] = [
    [
        sg.Text("Hello"),
    ],[ # End of row, beginning of the next one
        sg.Text("World"),
    ]
]
```
![](../assets/images/2025-08-05-13-25-08.png)

Notice how every list inside the layout-list is its own row.

# Making the layout look good
The normal "theme" doesn't look that good, I know.

To make it look better, simply apply a pre-made theme, like that:
```py
import SwiftGUI as sg
sg.Themes.FourColors.Emerald()
```
Just leave that on the top of your script and forget about it.

Themes are explained in-depth in the next tutorial, but applying them is as easy as that.

My personal favorites are:
```
sg.Themes.FourColors.FourColors.Emerald
sg.Themes.FourColors.FourColors.DarkTeal
sg.Themes.FourColors.FourColors.DarkCoffee
sg.Themes.FourColors.FourColors.SinCity
sg.Themes.FourColors.FourColors.Jungle
sg.Themes.FourColors.FourColors.DarkGold
```

Preview all available themes by calling `sg.Examples.preview_all_themes()`.

# Basic elements

There are a couple of elements you can choose from.

They each have a ton of options you can use to customize the element, but we will only focus on the common ones in this tutorial.

Pro-tipp: Preview all available elements by calling `sg.Examples.preview_all_elements()`.

## Text
This element allows you to display some text inside your GUI (Who would have guessed...).
`sg.Text` is the actual class, but I would use its alias `sg.T`. Does the exact same thing.

Like most elements, texts have a lot of options to customize them.

Consider this example:
```py
layout:list[list[sg.BaseElement]] = [
    [
        sg.T(
            # \n is the newline-character and will add a line-break
            "I'm a text.\nI have a couple of options you should know about...",
            width=60,   # Reserve space for 30 characters long, no matter how long the text actually is
            background_color=sg.Color.gold,    # Background-color
            text_color=sg.Color.navy,  # Text/font-color

            fonttype=sg.font_windows.Comic_Sans_MS, # Who doesn't like comic-sans?
            fontsize=14,    # Size of the text
        )
    ]
]
```
It will generate this window:\
![](../assets/images/2025-08-05-13-26-19.png)\
As you can see, swiftGUI provides pre-made colors and fonts (only for windows atm). 

Preview all colors by calling `sg.preview_all_colors()`.\
You can also use custom colors, by either entering a hex-code (e.g.: `#FF0020`), or using the rgb-function (e.g.: `sg.rgb(255, 0, 32)`).

## Input
Inputs allow the user to enter one-lined texts into your GUI.
You may use the alias `sg.In`, or `sg.Entry` instead of `sg.Input`, it's the same thing.

You can reuse most of the options from `sg.Text`, since both elements display a text:
```py
layout:list[list[sg.BaseElement]] = [
    [
        sg.In(
            "This will be displayed in the beginning",
            width=60,   # Reserve space for 30 characters long, no matter how long the text actually is
            background_color=sg.Color.gold,    # Background-color
            text_color=sg.Color.navy,  # Text/font-color

            fonttype=sg.font_windows.Comic_Sans_MS, # Who doesn't like comic-sans?
            fontsize=14,    # Size of the text
        )
    ]
]
```

![](../assets/images/2025-08-05-13-45-48.png)

How to actually read what the user wrote in there will be explained later.

It is possible to make this element "readonly", doing exactly what you think it does.
The user will still be able to copy the text inside, but can't change it.
That's pretty useful if you just want to display values for the user.
You could use `sg.Text` instead, but `sg.Input` looks better and the text can be copied by the user.

## Button

`sg.Button` creates a button the user can press to trigger an event.
How to use events to actually do something useful with it will be explained later.

Many options for it are the same as for `sg.Text`, because buttons usually display a text:
```py
### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.T("My button:")
    ],[
        sg.Button(
            "Push me!", # Button-text
            fonttype=sg.font_windows.Comic_Sans_MS, # I still like comic-sans
            fontsize=14,    # Bigger
            font_underline=True,    # Underline the text
            width=20,   # Width in characters
            height=5,   # Height in rows
            background_color=sg.Color.cadet_blue,   # Color of the button
            background_color_active=sg.Color.gold,  # While pressing the button, it turns "golden"
        )
    ],[
        sg.T("Amazing!")
    ]
]
```

![](../assets/images/2025-08-05-13-49-35.png)

Buttons have a ton of additional options.
Like setting a bitmap (image) as the button-text:
```py
### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.T("My button:")
    ],[
        sg.Button(
            bitmap="hourglass",
            text_color=sg.Color.red,
            width=25,
            height=25,
        )
    ],[
        sg.T("Amazing!")
    ]
]
```
![](../assets/images/2025-08-05-13-50-26.png)

It really pays off to read the documentation (once I am done writing it...).

Available bitmaps are proposed by the autocomplete-feature of your IDE (tested it in PyCharm), usually by pressing `Ctrl + Space` inside an empty string:

![](../assets/images/2025-08-05-13-51-03.png)

# Breaking out of the loop (events)

Remember this part of your template:
```py
### Main loop ###
for e,v in w:
    ...
```
As you might have noticed, the script will get stuck here.
The for-loop somehow won't execute.

That's because you need to "throw" an event to go through the loop a single time.

There are a couple of ways to set up events:
- Using event-elements like `sg.Button`
- Enabling the default-events for interactive elements like `sg.Input`, `sg.Table`, `sg.Checkbox`, etc.
- Binding custom events
- Throwing events manually from a different thread
- (Using the binding decorator)

All of these ways have something essential in common: **You have to set a key to throw an event to the event-loop!**\
Not setting a key can also be useful sometimes, but that's a different topic.

Whenever an "keyed-"event gets thrown, `e` ("event") will be set to the corresponding key (See the examples below).
The loop will then execute once.

## Using buttons, or default events
A button already comes with a builtin event.
Just set a key and you are good to go:
```py
import SwiftGUI as sg

### Global options ###


### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.Button(
            "Button 1",
            key="B1",
            fontsize=14,
        ),
        sg.Button(
            "Button 2",
            key="B2",
            fontsize=14,
        )
    ]
]

w = sg.Window(layout)

### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    print("Event:", e)

    if e == "B1":
        print("Button 1 was pressed!")

    if e == "B2":
        print("Button 2 was pressed!")

### After window was closed ###
```
This structure is the basic idea behind SwiftGUI (To be fair, it is very simmilar to the PySimpleGUI event-loop, but has a lot of advantages).
You now know how to differentiate between events and execute code accordingly.

To not slow down your code by throwing too many events, elements like `sg.Input` won't naturally throw events.
You have to specifically ask for it:

Any element the user can interact with in some way (`sg.Input`, `sg.Checkbox`, etc.) has the parameter `default_event`.
Set this to `True` and an event will be thrown as soon as the user changes the value of that element.

What exactly the user has to do is dependent on the type of element, but obvious most of the time.

**Remember to set a key,** or no event will be thrown to the event-loop.
```py
import SwiftGUI as sg

### Global options ###


### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.In(
            fontsize=20,
            default_event=True,
            key="Input"
        )
    ]
]

w = sg.Window(layout)

### Additional configurations/actions ###


### Main loop ###
for e,v in w:
    print("Event:",e)

    if e == "Input":
        print("The sg.Input was changed!")

### After window was closed ###
```

How to actually read what was written into the `sg.Input` will be explained later.

## Binding custom events
SwiftGUI is based on `tkinter`, a builtin Python-package.
`tkinter` offers a lot of different events you can throw: [TKinter reference](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/event-types.html).
You don't need to know most of these, but it can be useful to know what's possible.

"Binding" events is done via the corresponding event-string, some of which are listed in the linked tkinter-reference.
To make your life easier, SwiftGUI offers the class `Event`, which contains common event-strings.

Bind an event by calling `.bind_event` on the element-instance.
To make your life even more easier, `.bind_event` returns the instance itself, so you can call it directly inside your layout:
```py
### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.In(
            fontsize=20,
            default_event=True,
            key="Input"
        ).bind_event(sg.Event.ClickAny).bind_event(sg.Event.MouseEnter)
    ]
]
```
Now, the `sg.Input`-element will not only throw an event once its text changed (`default_event = True`), but also when any mouse-button is clicked on it (`.bind_event(sg.Event.ClickAny)`), or the mouse simply enters the element (`.bind_event(sg.Event.MouseEnter)`).

Unfortunately, any of these events will throw the same key: `"Input"`.
To keep them apart, you can use the parameters `key_extention` or `key` of `bind_event`:
```py
yourElement.bind_event(sg.Event.ClickAny,key_extention="_Click").bind_event(sg.Event.MouseEnter,key="MouseEnter")
```
`key_extention` will be appended to the normal key, so the `ClickAny`-event will throw `Input_Click`.\
`key` replaces the key all together, so the `MouseEnter`-event will throw `MouseEnter`.

## Throwing events from different threads
Threading can be tricky for Python-beginners.
If you don't know how to use threading, skip this part.
There is an in-depth explanation of these features in an advanced tutorial (if you don't see a link here, I forgot to add it...).

Call `w.throw_event(key)` on a different thread to throw an event.

You can also pass a value (`w.throw_event(key, value)`), which will be added to the value-dict (explained later) under the given key.

The value stays in the value-dict until you change it by throwing an event to the same key.

If you use a key that is already "occupied" by an element, the value will not transfer.

# Reading and changing values
In swiftGUI, you can read and write values pretty easily.

Reading: `w[key].value`\
Writing: `w[key].value = new_value`, or `w[key].set_value(new_value)`\
(`w` is a reference to the window-object)

What exactly you are reading/writing depends on the type of element.
For `sg.Input`-Elements, `w[key].value` returns/changes the text shown to the user.
Its type is `str`.

In my opinion, it's fairly obvious, what type the value has.
But I am adding a lot of typehints to make it as easy as possible for you.

Universal rule for any element: Reading and writing values always relates to the same thing.
If reading returns the text inside the element, writing it will change that text.\
E.g.: Reading the value of a `sg.Checkbox` returns if the box is checked or not. Writing it will check/uncheck the box.

Note that for `w[key]` to work, the element needs a key.
If you don't specify a key, the element can't be accessed this way.
If two elements share the same key (which you shouldn't do, but who am I to stop you), only one of these elements will be accessible through `w`.

The sole purpose of `w[key]` is to return the element you put into the layout, so you could just save it in a variable before putting it in:
```py
### Layout ###
my_text = sg.T("Hello World")
layout:list[list[sg.BaseElement]] = [
    [
        my_text
    ]
]

w = sg.Window(layout)

### Additional configurations/actions ###
my_text.value = "Hello GitHub"
```

For better readability, I recommend the walrus-operator (Not making up the name).
This code does exactly the same as before:
```py
### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        my_text := sg.T("Hello World")
    ]
]

w = sg.Window(layout)

### Additional configurations/actions ###
my_text.value = "Hello GitHub"
```

To make life easier for users transitioning from PySimpleGUI, all "keyed" values are saved inside `v` (`for e,v in w`), something that can be used simmilar to a dictionary.

`v[key]` is the same as `w[key].value`, so `v[key] = new_value` the same as `w[key].value = new_value`.

You can `print(v)`, which will print `v` like a dictionary.
However, this "collects" the value of every keyed elements, so you should only do it for debug reasons and remove it later.

This collecting-mechanism is a bit too complicated for this tutorial.
Let's just simplify: Every value is "fully collected" only once per loop.
That means, calling `print(v)` only really "hurts" once per loop.

It also means, `print(v)` might not contain values that got updated by `w[key].value = ...`.

However, `v[key]` is very reliable and always returns the correct value.

(Unnecessary side-rant about PySimpleGUI) In PySimpleGUI, `v` (or `value`) is a normal dictionary that completely updates once per loop.
That means, changing the value of elements won't update `value`.
Doesn't sound like much, but it annoyed the s out of me.

# Updating the layout
You can change most of the configuration of layout-elements after creating the window.
This way, you could e.g. make buttons change color, disable Input-elements, make text jump from one side to another, etc.

To update an element, get the reference (you could use `w[key]`) and call `.update` on it.
`.update` accepts most of the parameters the element itself accepts and if not, Python will tell you.

Unfortunately, `.update` doesn't suggest parameters yet, but I'm working on it.
However, the parameters are the same as creating the Element.

Examples:

To update the background-color of some Element from a previous example:
```py
w["Input"].update(background_color = sg.Color.red)
```

To disable a button (button can't be clicked anymore):
```py
w["ButtonKey"].update(disabled = True)
```
You get the idea...

## Reading/getting element-options
The "opposite" of `.update(key= ...)` is `.get_option(key)`.

`.get_option` returns whatever value you set that option (key) to earlier.

Why you would use that, if you know what you put in `.update`?\
Well, `.get_option` also returns values that are set by default.

E.g.: Not sure of the standard background-color?
Just use `.get_option`.

If you know tkinter: 
`.get_option` also returns options from the underlying tkinter-widget, if the option is unavailable otherwise.

E.g.: The option for background-color is called `background_color` in SwiftGUI, but `bg` in Tkinter.
That means, `.get_option("bg")` will return that configuration directly from the tkinter-widget using `tk_widget.cget(key)`.

# Where to now?

This library offers A LOT more while still being easy to use.

I highly recommend reading every basic tutorial.
You will be able to use the library pretty well just from these.

The Elements (widgets) itself also have a lot more functionality than you'd expect.
You might have been implementing features that are already implemented, because you didn't know they existed.\
If you want to dive deeper into that, read the Element tutorials.

The advanced tutorials explain how the package itself works, so you will be able to create your own widgets, or even packages that derive from SwiftGUI.

If you have any questions, feel free to ask them in the GitHub Forum.
I also appreciate ideas and ciricism.

Have fun!
