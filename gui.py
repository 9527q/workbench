import tkinter as tk
from tkinter import ttk

root_box = tk.Tk()

start_button = tk.Button(root_box, command=lambda: print("hhhh"), text="开始")

start_button.pack()


# 进入消息循环
root_box.mainloop()
