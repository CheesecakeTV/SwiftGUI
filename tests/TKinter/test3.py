import tkinter as tk
from pprint import pprint

root = tk.Tk()

l1 = tk.Label(text="Hallo Welt")
l1.grid()

pprint(list(l1.configure().keys()))

for i in range(5):
    tk.Label(text="Hallo Welt").grid()

root.mainloop()

