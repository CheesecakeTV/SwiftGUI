import tkinter as tk
import tkinter.ttk as ttk


root = tk.Tk()


my_button = tk.Button(root, text="Hallo Welt")
my_button.pack()

mb = ttk.Menubutton(root, text="Menü")
mb.pack()

my_menu = tk.Menu(mb)
mb["menu"] = my_menu

my_menu.add_checkbutton(label="Test")
my_menu.add_checkbutton(label="Hello")

root.mainloop()
