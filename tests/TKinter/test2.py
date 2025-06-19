import tkinter as tk

root = tk.Tk()
root.grid()

tk.Label(root,text="Hallo Welt").grid(row=0,column=0)
tk.Label(root,text="Hallo Welt").grid(row=1,column=1)
tk.Label(root,text="Hallo Welt").grid(row=2,column=0)
tk.Label(root,text="Hallo Welt").grid(row=3,column=0)



root.mainloop()
