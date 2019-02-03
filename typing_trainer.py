import tkinter as tk


class TrainText(tk.Text):
    def __init__(self):
        super().__init__(top_frame, wrap=tk.WORD, undo=0, bg="white",
                         font=('helvetica', 18), yscrollcommand=vbar.set)
        self.insert(tk.END, train_text)
        self.config(state=tk.DISABLED)

        self.tag_config("good", background="white", foreground="green")
        self.tag_config("cursor", background="yellow", foreground="black")
        self.mark_set("cursor_mark", "0.0")
        self.set_cursor()

        self.bind_all('<Key>', self.type)

    def type(self, event):
        self.remove_cursor()
        self.move_cursor_mark()
        self.set_cursor()
        self.tag_add("good", 0.0, 'cursor_mark')

    def move_cursor_mark(self):
        line, column = tuple(map(int, str.split(self.index('cursor_mark'), ".")))
        self.mark_set("cursor_mark", "%d.%d" % (line, column + 1))

    def remove_cursor(self):
        self.tag_remove("cursor", "cursor_mark")

    def set_cursor(self):
        self.tag_add("cursor", "cursor_mark")


# Create main window
root = tk.Tk()
root.minsize(70, 38)
# Create frames in window
bottom_frame = tk.Frame(root,width=100,height=100)
bottom_frame.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH)
top_frame = tk.Frame(root,width=100,height=100)
top_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
# Create quit button
bt = tk.Button(bottom_frame, text='Quit', command=root.destroy)
bt.pack(side=tk.BOTTOM)
bt.pack(side=tk.RIGHT, padx=10, pady=5)
# Define train text
train_text = "A general theory of cookies may be formulated this way. Despite its descent from cakes and other sweetened breads, the cookie in almost all its forms has abandoned water as a medium for cohesion. Water in cakes serves to make the base (in the case of cakes called batter) as thin as possible, which allows the bubbles - responsible for a cake's fluffiness - to better form. In the cookie, the agent of cohesion has become some form of oil."
# Define text box with scrollbar
vbar = tk.Scrollbar(top_frame,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)
train = TrainText()
train.pack(expand=True, fill="both")
vbar.config(command=train.yview)
# Mainloop
root.mainloop()
