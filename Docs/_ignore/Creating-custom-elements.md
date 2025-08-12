
# WIP
**Don't read!**

This documentation is old and only contains notes for me.

It will be improved in the future.

# Introduction

I tried to keep it as easy as possible to create custom elements you can easily use in your layout.
It's easy, but not straight-forward. You won't know how to do it just by reading my code.
That's where this explanation comes in handy.

I differentiate between the following types of elements:
- `Widgets`, which just contain a single tk-widget (or ttk-widget) with nothing fancy going on
- `Custom widget`, which contain a single tk-widget, but do some crazy things automatically
- `Widget-container`, which contain and manage multiple elements. **You don't need to know tkinter to define one of those**

# Default options


# Widgets
The easiest case.

If you just want to wrap a widget, so it fits into sg-layouts, use the following template:
```py
class Example(BaseWidget):
    _tk_widget_class = tk.Label  # Class of your tk-widget, Label (text) in this case
```

That's it. Now you can have a `tk-widget` living inside the sg-window:

```py
import SwiftGUI as sg

layout = [
    [
        sg.Example(text="It does work...")
    ]
]
w = sg.Window(layout)
w.loop()
```
![image](https://github.com/user-attachments/assets/e4694dc8-a142-4908-a678-1ef6a01f7a09)

You can set a key and use `.update()` on this element, but `.value` doesn't work, because it doesn't know how to get the value.

If you really need to extract the value, access the widget through `instance.tk_widget` and "fish it out":
```py
import SwiftGUI as sg

layout = [
    [
        sg.Example(key="MyText",text="It does work..."),
    ],[
        sg.Button(text="Generate event",key="Hi")
    ]
]

w = sg.Window(layout)
print(w.loop()) # Key MyText will be None
print(w["MyText"].tk_widget["text"])    # This works
```
The value won't show up as a return of `w.loop()` though and it's kinda annoying to get to the value like that.

Not a big deal for a text (aka label), but keep in mind that widgets like Input (Entry), where the user inputs something, can't be read in the usual way neither.

## Easy generic way to "define" the value
Most tk-widgets allow you to set a target-variable to store the current value.

By default, SwiftGUI tries to access this target-variable when reading the value of an element.
Of course, there is an easy way to set this variable:
```py
class Example(BaseWidget):
    _tk_widget_class = ttk.Label  # Class of your tk-widget
    defaults = GlobalOptions.DEFAULT_OPTIONS_CLASS      # Default options to be applied

    def _personal_init_inherit(self):
        self._set_tk_target_variable(tk.StringVar,"textvariable", default_key="text")
```
`_personal_init_inherit` is called automatically before the widget is initialized.

To set the variable, `self._set_tk_target_variable` is used:
- First argument is the type of variable. tkinter has four: `StringVar`, `IntVar`, `BoolVar` and `DoubleVar`
- Second argument is the variable-key of the tkinter-widget. This can differ from widget to widget. For `tk.Label`, it is `"textvariable"`.
- `default_key` is used to determine the starting-value (aka default-value). Since we create the widget using `sg.Example(key="MyText",text="It does work...")`, the key is `"text"`. Just take whatever the parameter is called.
- `default_value` may be used to set a literal starting-value, which is set, when `default_key` doesn't exist.

Now, the Example-Element works correctly and we can even change the text using `instance.value`:
```py
import SwiftGUI as sg

layout = [
    [
        sg.Example(key="MyText",text="It does work..."),
    ],[
        sg.Button(text="Generate event",key="Hi")
    ]
]

w = sg.Window(layout)
print(w.loop()) # 'MyText': 'It does work...'
print(w["MyText"].value)    # This works too
w["MyText"].value = "Changed!"  # Value changes next time w.loop() is called
w.loop()
```

## Changing keys
Sometimes, the tk-key isn't as clear as it should be. It would be nice to decide how to call it yourself.

That's why SwiftGUI let's you "transfer" one key to another quite easily.
Just add the `_transfer_key`-attribute (dictionary) to your class.

`Key` will be where to transfer from (what the user enters), `val` where to transfer to (the tkinter-key).


# Custom widgets
This is where the fun begins!

You can create your own custom widget from scratch, but I'd recommend just deriving it from an existing widget.

...


## Useful methods/attributes to overwrite
These attributes where created for the sole purpose of overwriting them.

**Remember: Some of them still need their super-method to be called.**
### _get_value()
The return of this method is returned when you read the `value` attribute.
It's the proper way to tell SwiftGUI, which value this element has at the moment.

### set_value(val)
Guess what this does...

### defaults
Class derived from `GlobalOptions.DEFAULT_OPTIONS_CLASS`.
Used to set options per default.
See [default options](Creating-custom-elements#default-options) for more details.

### _flag_init()
A good place to set default element-flags.
Almost the beginning of the init-procedure.

### _personal_init_inherit()
A good place to do whatever you want right before the tk-widget is initialized.

### _init_widget_for_inherrit()
**Dont' forget the super-call, and return it!**\
Only does one thing: Call the widget-class (`_tk_widget_class`) to instantiate the actual tk-widget.

If you are to lazy to work yourself through this big structure of methods, you may use this one instead.
Very straight-forward.

### _update_special_key()
When you use `.update`, or initialize the element, all "updated" keys will be passed through ("unfiltered") to the tk_widget.

But before they will go through `_update_special_key` one by one.
This way, you can add more complex functionality to certain keys.

**To exclude a key from being passed to the tk_widget, return anything inside this function!**

An implementation might look like this:
```py
    def _update_special_key(self,key:str,new_val:any) -> bool|None:
        # Fish out all special keys to process them seperately
        match key:
            case "font_underline":
                self._underline = self.defaults.single(key,new_val)
                self.add_flags(ElementFlag.UPDATE_FONT)

            case "text_color":
                # Replace the key "text_color" with "foreground", because "text_color" is much easier to interpret
                self._tk_kwargs["foreground"] = self.defaults.single(key,new_val)

            case _: # Not a match, so the key won't be picked out
                return False

        return True # Key matched, so pick it out, don't pass it to tk_widget
```

### _apply_update()
**Don't forget the super-call!**

Applies all performed updates from a single `.update()` call.
Great place to do something before/after persisting the update.


## Useful methods/attributes to use

### window
References the `sg.Window` this element is in

### parent
References the next-higher sg-element

### add_flags(), remove_flags(), has_flag()
These can be used to set element-flags (States this element is in).
Create custom flags by deriving from `ElementFlag`:
```py
from SwiftGUI import ElementFlag

class MyFlags(ElementFlag):
    IS_MY_FLAG = 100 # Start with 100, flags before 100 are reserved for me!
    IS_ANOTHER_FLAG = 101
```
You can achieve the same by creating bool-attributes inside your custom-widget, but flags are a little less annoying to handle.

### bind_event()
Standard user-function.
See user-guide for further information.



