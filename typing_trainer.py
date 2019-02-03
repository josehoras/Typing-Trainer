import tkinter as tk


def quit(event):                           
    root.destroy()
def typing(event):
    key = event.keysym
    train.config(state=tk.NORMAL)
    train.insert(tk.END, key)
    train.config(state=tk.DISABLED)
    index = train.index(tk.INSERT)
    print(index)
    train.mark_set("insert", index)
    # pos = my_canvas.itemcget(1, "bbox")
    # pos = my_canvas.bbox(1)
    #my_canvas.itemconfig(1, text=my_canvas.itemcget(1, "text") + key)




# Create main window
root = tk.Tk()
root.minsize(70, 38)
# Create frames in window
bottom_frame = tk.Frame(root,width=300,height=300)
bottom_frame.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH)
top_frame = tk.Frame(root,width=300,height=300)
top_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
# Create quit button
bt = tk.Button(bottom_frame, text='Quit')
bt.pack(side=tk.BOTTOM)
bt.pack(side=tk.RIGHT, padx=10, pady=5)
# Create canvas with scrollbar to put text
# vbar = tk.Scrollbar(top_frame,orient=tk.VERTICAL)
# vbar.pack(side=tk.RIGHT,fill=tk.Y)
# vbar.config(command=my_canvas.yview)

# Create text on canvas (item number 1)
train_text = "A general theory of cookies may be formulated this way. Despite its descent from cakes and other sweetened breads, the cookie in almost all its forms has abandoned water as a medium for cohesion. Water in cakes serves to make the base (in the case of cakes called batter) as thin as possible, which allows the bubbles - responsible for a cake's fluffiness - to better form. In the cookie, the agent of cohesion has become some form of oil."
# train_text = "a"
input_text_good = ""
input_text_wrong = ""

vbar = tk.Scrollbar(top_frame,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)

train = tk.Text(top_frame, wrap=tk.WORD, undo=0, bg="white", yscrollcommand=vbar.set)
train.pack(expand=True, fill="both")
vbar.config(command=train.yview)

# train.tag_add("good", 1.4)
train.tag_config("good", foreground="green")
train.insert(tk.END, train_text)
train.config(cursor="arrow")
train.tag_add("good", 1.4, 1.6)
train.mark_set("insert", "%d.%d" % (1, 6))
train.config(state=tk.DISABLED)


# Define bindings
bt.bind('<Button-1>', quit)
root.bind('<Key>', typing)
# Mainloop
root.mainloop()
