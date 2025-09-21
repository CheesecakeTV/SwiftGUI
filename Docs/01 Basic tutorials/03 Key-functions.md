This is a very useful feature of `SwiftGUI` I really miss in `PySimpleGUI`.

Don't get me wrong, the event-loop-system is great for smaller windows, but for bigger GUIs, you don't want to set and handle each and every tiniest action by running through the whole loop.
Every event needs its own entry inside the giant event-loop and everything gets real messy real fast.

Example: You'd like to create an input-field with a small button on the side that clears the input.
The only purpose of the button is to clear the input, yet it enlarges the event-loop.
It also needs its own unique key, which makes things complicated when you want to copy that part of the layout.

The solution: Define the action (function) to do when creating the element, using key-functions.

# Basic concept

When creating elements, or binding events, you don't actually need to specify a key to throw events.
If you define a key-function, that function will be called when the event occurs.
You do not need to define a key if you define at least one key-function.

Example: Let's create a button that prints "hello world" to the console when pressed:
```py
import SwiftGUI as sg

def hello_world():
    print("Hello World")

### Global options ###

### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.Button(
            "Print hello World!",
            key_function=hello_world
        )
    ]
]

w = sg.Window(layout)

### Additional configurations/actions ###

### Main loop ###
for e,v in w:
    ...

### After window was closed ###
```
That's all you need.
The main loop is still empty, yet the `hello_world` is called when the button is pressed.

For a small functionality like this you might want to use a lambda-function instead:
```py
layout:list[list[sg.BaseElement]] = [
    [
        sg.Button(
            "Print hello World!",
            key_function=lambda :print("Hello World")
        )
    ]
]
```

You can also add more than one key-function by putting them inside a list/tuple:
```py
sg.Button(
    "Print hello World!",
    key_function=[
        lambda: print("Hello World"),
        lambda: print("Another key-function!"),
    ]
)
```

**You can also add key-functions to custom events using `.bind_event` on the element.** (Remember this, it's important)

# Parameters
This feature looks pretty basic so far.
The functions seem to only be able to do the exact same thing every call.

Here's the best part about key-functions:
You can "request" certain information about the GUI by using parameters.

If you create parameters with these names, they will be written accordingly:
- `w`     - Window (the window, called `w` in the template)
- `e`     - Event (Event-key, if you did define it, same as `e` of the template)
- `v`     - Value-"dict", same as `v` in the for-loop
- `val`   - Value (Value of the event-element, same as `w[key].value` if you set a key)
- `elem`  - Element (Element that caused the event, same as `w[key]`, if you set a key)

Example: Let's create an input-element that prints its value to the console after being changed:
```py
### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.In(
            default_event=True,
            key_function=lambda val:print("New value:",val),
        )
    ]
]
```
Because the parameter of the lambda-function is called `val`, the current value (`element.value`) is passed to `val`.

Another example: Let's change the inputs background-color depending on weather an input number is odd or even:
```py
### Global options ###
def change_if_value_is_even(val, elem):
    try:
        if int(val) % 2 == 0:   # Even
            elem.update(background_color = sg.Color.sea_green)
        else:
            elem.update(background_color=sg.Color.light_blue)
    except ValueError: # Not a number
        elem.update(background_color=sg.Color.orange)


### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.In(
            default_event=True,
            key_function=change_if_value_is_even,
        )
    ]
]
```
Try it yourself, it works perfectly.

The best part is, we can simply duplicate the input-element while preserving its functionality:
```py
### Layout ###
layout:list[list[sg.BaseElement]] = [
    [sg.In(default_event=True,key_function=change_if_value_is_even)],
    [sg.In(default_event=True, key_function=change_if_value_is_even)],
    [sg.In(default_event=True, key_function=change_if_value_is_even)],
    [sg.In(default_event=True, key_function=change_if_value_is_even)],
    [sg.In(default_event=True, key_function=change_if_value_is_even)],
]
```

![](../assets/images/2025-08-05-14-52-03.png)

Keep in mind that the actual event-loop is still empty and we did not use any key so far.

# Pre-made KeyFunctions

Some key-functions are pretty common (at least for me).
You will likely write them over and over again for different projects.

That's why `SwiftGUI` includes a bunch of common key-functions and "key-function-templates".

Every one of them has its own docstring, you can find them [here](https://github.com/CheesecakeTV/SwiftGUI/blob/c573a78ee0fa9ea5565a76556aeba9d930dc98f4/src/SwiftGUI/KeyFunctions.py).

Example: We can use a key-function to implement the example mentioned at the beginning of this tutorial.
Let's create an input-element that can be cleared by pressing a button:
```py
### Layout ###
layout:list[list[sg.BaseElement]] = [
    [
        sg.In(
            key="Input"
        ),
        sg.Button(
            "Clear",
            key_function=sg.KeyFunctions.set_value_to(elem_key="Input")
        )
    ]
]
```
If we look at `sg.KeyFunctions.set_value_to`, we can see that it is a function returning another function.
The returned function is the actual key-function and looks like this:
```py
def temp(v):
    v[elem_key] = new_value
```
Simple, yet elegant and very useful.

Get used to using key-functions, they are truly awesome.

By the way, I'm the most humble person in the world. Noone knows humble better than me.

# Chaining key-functions
Instead of a single key-function, you may pass a list (or any iterable) of multiple functions, as mentioned above.
These functions will be called one after another.

**There is a nasty trap to this:** `val` will only be refreshed, after all key-functions of an element are executed (for performance reasons).

So, if your first key-function multiplies `val` by 2 and the next one divides by 10, the division uses the same "starting-value" as the multiplication.
That means, the multiplication has no effect.

**This is only a problem if a single element has multiple key-functions.**

But there's hope! If your key_function returns anything but None, all values will be refreshed directly after execution.

# Decorating functions to make them key-functions
Big thanks to [yunlo](https://github.com/yunluo) for this idea!

I tried really hard to find any advantage of this method over standard key-functions, but couldn't.
It's just a different way to structure your code, which you might like better.

Using a certain decorator, you can assign key-functions to a key in the event-loop.
When the event-loop receives that key in an event, the key function will be called **instead of running through the loop**:
```py
import SwiftGUI as sg

@sg.attach_function_to_key("Button1")
def do_something():
    print("Button 1 was pressed")

@sg.attach_function_to_key("Button2")
def do_something_else(v):
    print("Button 2 was pressed.")
    v["Button2"] = "Pressed"

layout = [
    [
        sg.Button(" 1 ", key="Button1"),
        sg.Button(" 2 ", key="Button2"),
        sg.Button(" 3 ", key="Button3"),
    ]
]

w = sg.Window(layout)

for e,v in w:
    print("Loop:",e, v)
```
Best to copy the code and try yourself:
- When b1 is pressed, `do_something` is called.
The loop does not run.
- When b2 is pressed, `do_something_else` is called and the value-dict is passed to `v`.
The loop does not run here either.
- The key of b3 isn't used in any of the decorators, so the event-loop runs normally.

Other than actual key-functions, these "decorated functions" should only take `e`, `v`, or `w` as parameters.
`elem` and `val` will always be `None`.

It is also possible to attach multiple keys using the decorator:
```py
@sg.attach_function_to_key("Button1", "Button2")
def do_something(e):
    print(f"{e} was pressed")
    v[e] = "Pressed"
```

Some things to keep in mind when using this feature though:
- All "decorations" must be done before creating the window using `w = sg.Window(layout)`
- The decorator only applies to the main event-loop.
Since SwiftGUI version 0.8.0, it is possible to create other event-loops.
Keys for these loops are not affected.
- If you create multiple windows using `sg.Window` in a single program (which has risks on its own), the decorated functions apply to all windows.
Also, the parameter `w` will always hold the first window created.
So better avoid reusing decorator-keys, even through different windows.\
There will be a way to create additional windows before version 1.0.0, I promise!
- Don't decorate multiple functions with the same key. Only the last declared function will be called.


