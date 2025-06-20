import tkinter as tk

fenster = tk.Tk()
fenster.title("Hallo Welt")
# tk.Label(fenster,text="Test").pack(side="left")
# tk.Button(fenster,text="Hallo Welt",command=lambda :print("Hallo")).pack(side="right")

f1 = tk.Frame(fenster, relief="sunken", bd=3)
f2 = tk.Frame(fenster, relief="raised", bd=3)

tk.Label(f1,text="Test",width=10).grid(row=0,column=0)
tk.Button(f1,text="Hallo Welt",command=lambda :print("Hallo")).grid(row=0,column=1)
tk.Label(f1,text="Test").grid(row=1,column=0)
tk.Button(f1,text="Hallo Welt",command=lambda :print("Hallo")).grid(row=1,column=1)

tk.Label(f2,text="Test").grid(row=2,column=0)
tk.Button(f2,text="Hallo Welt",command=lambda :print("Hallo")).grid(row=2,column=1)

f1.pack(side="left",padx=10)
f2.pack(side="right")

fenster.mainloop()
