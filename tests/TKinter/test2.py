import tkinter as tk

root = tk.Tk()
root.grid()

tk.Label(root,text="Hallo Welt").grid(row=0,column=0)
tk.Label(root,text="Hallo Welt").grid(row=1,column=1)
tk.Label(root,text="Hallo Welt").grid(row=2,column=0)
tk.Label(root,text="Hallo Welt").grid(row=3,column=0)

measureSystem = tk.StringVar()
check = tk.Checkbutton(root, text='Use Metric',
        variable=measureSystem,command=lambda :print(measureSystem.get()),
	    onvalue='metric', offvalue='imperial')
check.grid()

phone = tk.StringVar()
tk.Radiobutton(root, text='Home', variable=phone, value='home', command=lambda :print(phone.get())).grid()
tk.Radiobutton(root, text='Office', variable=phone, value='office', command=lambda :print(phone.get())).grid()
tk.Radiobutton(root, text='Mobile', variable=phone, value='cell', command=lambda :print(phone.get())).grid()

tk.Entry(root,  show="*").grid()

import re
def check_num(newval):
    return re.match('^[0-9]*$', newval) is not None and len(newval) <= 5
check_num_wrapper = (root.register(check_num), '%P')

num = tk.StringVar()
e = tk.Entry(root, textvariable=num, validate='key', validatecommand=check_num_wrapper) # vali... stops you from writing anything not covered by check_num
e.grid()

root.mainloop()
