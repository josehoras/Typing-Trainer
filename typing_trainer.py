import tkinter as tk


def quit(event):                           
    root.destroy()
def typing(event):
    global txt
    key = event.keysym
    txt = txt + key
    texto = my_canvas.find_withtag("texto")
    my_canvas.itemconfigure(texto, text=txt)
    
root = tk.Tk()
root.minsize(100, 100)

top_frame = tk.Frame(root,width=300,height=300)
top_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
bottom_frame = tk.Frame(root,width=300,height=300)
bottom_frame.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH)

bt = tk.Button(bottom_frame, text='Quit', height=3, width=3)
bt.pack(side = tk.BOTTOM)
bt.pack(side = tk.RIGHT, padx=10, pady=5)

my_canvas = tk.Canvas(top_frame, width=300, height=300, scrollregion=(0,0,300,500), bg="white")
vbar= tk.Scrollbar(top_frame,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)
vbar.config(command=my_canvas.yview)
txt = "hola"

my_canvas.config(yscrollcommand=vbar.set, yscrollincrement=10)
my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
my_canvas.pack(side=tk.TOP)
my_canvas.create_text(30, 70, text=txt, anchor='sw', width=200, font=('helvetica', 18), tag="texto")

# text_widget = tk.Text(bottom_frame, wrap=tk.NONE, undo=True, yscrollcommand=vbar.set)
# text_widget.pack(expand=True, fill="both")



bt.bind('<Button-1>', quit)
root.bind('<Key>', typing)


root.mainloop()
