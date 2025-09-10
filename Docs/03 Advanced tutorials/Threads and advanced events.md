
# What is multithreading?
If you already know how to use multithreading in Python, skip this part.

Multithreading is a way of running multiple programs at the same time.
They seem to run at the same time, but actually don't, but let's not get lost in the theory.

Very basically, you can create a thread and run a function on it, which will run "fake-parallel" to the rest of the script (main thread).

Copy and run this example:
```py
import threading
import time

def funct():
    while True:
        print("Hello")
        time.sleep(1)


my_thread = threading.Thread(target= funct, daemon= True) # Create the thread
my_thread.start()   # Start the new thread

time.sleep(0.5)
while True:
    print("World")
    time.sleep(1)
```
As you can see, "Hello" and "World" are printed alternating, even if both `func` and the `while`-loop should block the program.
Seems like the function runs in parallel to the script.

The `daemon`-keyword is very important.
If set to `Tread`, the thread will automatically stop, when the main script stops.
If you don't set it and stop the script, the thread will stay active in the background.

You can do a lot more with threading in Python.
Check it out in the [python-docs](https://docs.python.org/3/library/threading.html).


# Multithreading in SwiftGUI
Usually, the window blocks the script execution in the event-loop until an event occurs.

Using threading, you can execute code while the window is waiting for its next event.
You can even throw your own events.

This tutorial covers all you need to know to run background-threads properly.

# Basic "rules"
Create and start the threads **after** the window-creation **before** entering the event-loop:
```py
w = sg.Window(layout)

# Right here

for e,v in w:
    ...
```
This way, you can access `w` from inside the thread-function without any issue.
If you know more about threading, you should have no problem doing it differently though.

Don't change values or use `.update` from inside the thread.
It might work, but could very well crash your code instead.
The proper way to do this is explained later.

Reading values from is totally fine though.

Set `deamon= True`, so the thread stops executing when the window closes.

# Throwing events manually

## Key-event
The easiest event to throw is a key-event, where the key is written to `e` in the event-loop.

Just call `.throw_event(key= ...)` on the window:
```py
import SwiftGUI as sg
import threading
import time

### Global options ###

def fkt():
    while True:
        time.sleep(1)
        w.throw_event(key= "blink") # "blink" is written to e

### Layout ###
layout = [
    [
        my_text := sg.T("Some text", fontsize= 24), # Don't leave the layout empty
    ],
]

w = sg.Window(layout)

### Additional configurations/actions ###
threading.Thread(target= fkt, daemon= True).start() # Create and start the thread

### Main loop ###
for e,v in w:
    print(e, v) # blink {'blink': None}
```
As you can see, `"blink"` is written to `e` and the key is also added to the value-dict `v`.

If you'd like to specify the value, pass it to `.throw_event`:
```py
def fkt():
    while True:
        time.sleep(1)
        w.throw_event(key= "blink", value= 1) # v["blink"] = 1
        time.sleep(1)
        w.throw_event(key= "blink", value= 0) # v["blink"] = 0
```

After throwing a key-event, the key will stay in the value-dict until the program ends.

## Function-call
As I explained in the beginning, you really shouldn't change the value and options of elements from the thread, because it might cause the gui to crash.

That's why `.throw_event` can call a function for you:
```py
def fkt():
    while True:
        time.sleep(1)
        w.throw_event(function= my_text.set_value, function_args=(1, )) # = my_text.set_value(1), same as my_text.value = 1
        time.sleep(1)
        w.throw_event(function= my_text.set_value, function_args=(0, )) # = my_text.set_value(0)
```
(`.set_value(...)` is the same as `.value = ...`)

Keep in mind that this method does **not** offer the key-function functionality, where parameters called `e`, `v`, `w`, `elem`, or `val` will be automatically be passed.
You need to pass the parameters yourself with `function_args` and `function_kwargs`.

If you don't pass anything, the function will be called without parameters.

`function_args` takes a tuple, `function_kwargs` takes a dictionary:
```py
w.throw_event(function= print, function_args= ("Hello", "World"), function_kwargs= {"sep": " - "}) # = print("Hello", "World", sep= "-")
```

# Event-functions
Make sure you understand key-functions (see basic tutorial 03).

Behind every event is a so called event-function.
That event-function contains the key and all key-functions from that event.

When the event is thrown, this event-function is called **without any arguments**.
Combining an event-function with `.throw_event` will enable you to create custom events that function just like any other event in SwiftGUI.

Create an event-function using `w.get_event_function(...)`.
That method takes 3 optional arguments:
- `key`: Works the same as any event-key. If given, the event gets thrown to the event-loop
- `key_function`: Works the same as any `key_function`-parameter of any element
- `me`: An element passed will act as the event-throwing element. This element and its value will be passed to the key-function(s) under `elem` and `val`

### Some examples

Let's create an event-function that calls `print("Event called")` and modify the thread-function accordingly:
```py
def fkt():
    event_f = w.get_event_function(key_function= lambda: print("Event called"))
    while True:
        time.sleep(1)
        w.throw_event(function= event_f)
```

If `me` is passed, key-functions can use `elem` and `val`.
This thread-function will show the value of `n` in the `my_text`-element:
```py
def fkt():
    n = 0
    event_f = w.get_event_function(me= my_text, key_function= lambda elem: elem.set_value(n))
    while True:
        time.sleep(1)
        w.throw_event(function= event_f)
        n += 1
```
`e`, `v` and `w` are always available as parameters, even without passing `me`.

