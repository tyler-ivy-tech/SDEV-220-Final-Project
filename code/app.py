# Trying out Tkinter
# Tutorial: https://www.youtube.com/watch?v=3GkavfUnOQE

import tkinter
from tkinter import ttk
import tkinter.colorchooser

window = tkinter.Tk()
window.title("Library Management System")

def change_color():
    colors = tkinter.colorchooser.askcolor()
    window.configure(bg=colors[1])

ttk.Button(window, text="Pick Color", command=change_color).pack()

window.mainloop()