import tkinter as TK
from tkinter import ttk

root = TK.Tk()
# print(root.configure().values())
style = ttk.Style()

# Style
style.configure("BW.TLabel", foreground="black", background="white")
style.configure("RED.TButton", foreground="red", background="white")
print(style.element_names())


def turn_red(self, event):
    event.widget["activeforeground"] = "red"


frm = ttk.Frame(root, width=100, height=100, padding=50)
frm.grid()
lbl = ttk.Label(frm, text="Hello World!", justify=("center")).grid(column=0, row=0)
# print(lbl)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
btn = ttk.Button(frm, text="Quit", style="RED.TButton").grid(column=1, row=1)


root.mainloop()
