
This tutorial explains how to create a custom global-option class.

It's very easy, but not relevant for beginners.

# Why?

Some (one at the moment, version 0.5.0) of the advanced tutorials show how to create custom elements.

SwiftGUI offers high-level functionality to apply default values ("global options").
To create custom elements properly, you should also add a proper way to set default values for that new type of element, especially when the element is used often.

**Make sure to read basic tutorial 02: "Global options and Themes" before creating your own GO-class.**
That tutorial explains how the GO-classes behave.

# Creating the class
To make life easier, let's import the global options separately:
```py
import SwiftGUI as sg
import SwiftGUI.GlobalOptions as go
```

To create a GO-class, simply inherrit another GO-class.
As explained in the above mentioned tutorial, all options from that parent-GO-class will also be options in the new one.

If your class doesn't provide that option or sets it `None`, the parent option will be applied.

If you want to start "blank", inherrit from `go.DEFAULT_OPTIONS_CLASS`:
```py
class Example(go.DEFAULT_OPTIONS_CLASS):
    ...
```

## Providing options
To add options, just specify them as attributes:
```py
class Example(go.DEFAULT_OPTIONS_CLASS):
    width = 15
    height = 1
```

# Assigning the options to elements
## Custom elements
Simply assign the class to the attribute `defaults` of your custom class:
```py
class Example(go.DEFAULT_OPTIONS_CLASS):
    width = 15
    height = 1

class Example_element(sg.BaseElement):
    defaults = Example
```

## Existing elements
If you want, you can change the attribute `defaults` on existing classes, to assign a different go-class:
```py
class Example(go.DEFAULT_OPTIONS_CLASS):
    width = 15
    height = 1

sg.Text.defaults = Example
```

No idea why you would do that, but you can.

## Some elements of an existing type
There is no provided way to assign go-classes to specific elements only, but you can use this easy workaround.

Just inherrit a class from the existing element-class and change its `defaults`-attribute:
```py
class Example(go.DEFAULT_OPTIONS_CLASS):
    width = 15
    height = 1

class Text_Special(sg.Text):
    defaults = Example
```
`Text_Special` will behave exactly like `sg.Text`, but has the go-class `Example` instead.

It might be a good idea to derive `Example` from `go.Text` though, but that's up to you.

# How to apply global options
## The "automatic" way
Usually, global options are applied, when `.update` is called on an element.

This is also true for custom elements, as long as you don't mess with the update-routine maliciously.

If `.update` receives an argument with the value `None` (Like `.update(background_color = None)`), it will be replaced by the global option, if one is available.

## The "manual" way
GO-classes offer methods to manually apply global options.

### Single
For a single option, use `Example.single(key, value, default = None)`:\
If the value is not `None`, `value` will be returned.\
Otherwise, the go-class tries to provide the option (also searching through parent classes).\
If no value for that key can be found, `default` is returned.

Example:
```py
class Example(go.DEFAULT_OPTIONS_CLASS):
    width = 15
    height = 1

Example.single("width", 20) # Returns 20
Example.single("width", None) # Returns 15
Example.single("color", None, default= "red")   # Returns "red"
Example.single("color", "blue", default= "red")   # Returns "blue"
Example.single("color", None)   # Returns None
```

### Dictionary
`.apply(apply_to)` does the same as `.single`, only for multiple keys at once.
It is also not possible to specify an additional default-value (yet, version 0.5.0).

The passed argument is a dictionary.
Any value that is None gets replaced by the global option, if it exists.

**`.apply` will modify the provided dictionary itself** and returns it.
So if you want to keep the original one, use `.copy()` when passing the argument.

Example:
```py
class Example(go.DEFAULT_OPTIONS_CLASS):
    width = 15
    height = 1

test = {"width": 20, "height": None, "color": None}
Example.apply(test)
print(test) # {'width': 20, 'height': 1, 'color': None}
```
