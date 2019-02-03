#!/usr/bin/python3
# write tkinter as Tkinter to be Python 2.x compatible
import tkinter as tk
import sys

def hello(event):
    print("Single Click, Button-l") 
def quit(event):                           
    print("Double Click, so let's stop") 
    root.destroy()
def a(event):
    global txt
    key = event.keysym
    txt = txt + key
    texto = my_canvas.find_withtag("texto")
    my_canvas.itemconfigure(texto, text=txt)
    
root = tk.Tk()
my_frame = tk.Frame(root,width=300,height=300)
my_frame.pack(expand=True, fill=tk.BOTH)

my_canvas = tk.Canvas(my_frame, width=300, height=300, scrollregion=(0,0,300,500), bg="white")
vbar= tk.Scrollbar(my_frame,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)
vbar.config(command=my_canvas.yview)
txt = "hola"


my_canvas.config(yscrollcommand=vbar.set, yscrollincrement=10)
my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
my_canvas.create_text(30, 70, text=txt, anchor='sw', tag="texto")


bt = tk.Button(root, text='Quit')
bt.pack(expand=False, side = tk.BOTTOM)
bt.pack(side = tk.RIGHT, padx=10, pady=5)

bt.bind('<Button-1>', quit)
root.bind('<Key>', a)


root.mainloop()
