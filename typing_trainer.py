import tkinter as tk


def quit(event):                           
    root.destroy()

class TrainText(tk.Text):
    def __init__(self):
        super().__init__(top_frame, wrap=tk.WORD, undo=0, bg="white",
                         font=('helvetica', 18), yscrollcommand=vbar.set)
        self.tag_config("good", background="white", foreground="green")
        self.tag_config("cursor", background="yellow", foreground="black")
        self.insert(tk.END, train_text)

        self.good = 0
        self.set_cursor()
        # self.mark_set("insert", "%d.%d" % (1, self.good))
        self.bind_all('<Key>', self.type)

    def type(self, event):
        self.remove_cursor()
        self.good += 1
        self.set_cursor()
        tag_end = "%d.%d" % (1, self.good+1)
        self.tag_add("good", 0.0, tag_end)
        print(self.tag_ranges("good")[0])

    def remove_cursor(self):
        if self.tag_ranges("cursor"):
            self.tag_remove("cursor", self.tag_ranges("cursor")[0], self.tag_ranges("cursor")[1])

    def set_cursor(self):
        tag_init = "%d.%d" % (1, self.good)
        tag_end = "%d.%d" % (1, self.good+1)
        self.tag_add("cursor", tag_init, tag_end)
        print(tag_init, " ", tag_end)
        print(self.tag_ranges("cursor"))

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

# Create text on canvas (item number 1)
train_text = "A general theory of cookies may be formulated this way. Despite its descent from cakes and other sweetened breads, the cookie in almost all its forms has abandoned water as a medium for cohesion. Water in cakes serves to make the base (in the case of cakes called batter) as thin as possible, which allows the bubbles - responsible for a cake's fluffiness - to better form. In the cookie, the agent of cohesion has become some form of oil."
input_text_good = ""
input_text_wrong = ""

vbar = tk.Scrollbar(top_frame,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)

# train = tk.Text(top_frame, wrap=tk.WORD, undo=0, bg="white", yscrollcommand=vbar.set)
train = TrainText()
train.pack(expand=True, fill="both")
vbar.config(command=train.yview)

# train.tag_add("good", 1.4)

train.insert(tk.END, train_text)
# train.config(cursor="arrow")
# train.config(state=tk.DISABLED)


# Define bindings
bt.bind('<Button-1>', quit)
# root.bind('<Key>', typing)
# Mainloop
root.mainloop()
