import tkinter as tk

LETTERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
           'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p',
           'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
           'y', 'x', 'c', 'v', 'b', 'n', 'm',
           'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P',
           'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
           'Y', 'X', 'C', 'V', 'B', 'N', 'M']
SPECIAL_KEYS = {'degree': '°', 'asciicircum': '^', 'exclam': '!', 'quotedbl': '"',
                'section': '§', 'dollar': '$', 'percent': '%', 'ampersand': "&",
                'slash': "/", 'parenleft': '(', 'parenright': ')', 'slash': "/",
                'parenleft': '(', 'parenright': ')', 'equal': '=', 'question': '?',
                'grave': '`', 'space': " ", 'ssharp': "ß", 'acute': '´', 'plus': '+',
                'less': '<', 'comma': ',', 'period': '.', 'minus': '-', 'underscore': '_',
                'udiaeresis': 'ü', 'Udiaeresis': 'Ü', 'odiaeresis': 'ö', 'Odiaeresis': 'Ö',
                'adiaeresis': 'ä', 'Adiaeresis': 'Ä', 'asterisk': '*', 'numbersign': '#',
                'apostrophe': "'", 'colon': ':', 'semicolon': ';', 'greater': '>', 'at': '@'}

class TrainText(tk.Text):
    def __init__(self, frame, texts=[]):
        super().__init__(frame, wrap=tk.WORD, bg="white", height=8, width=50,
                         font=('helvetica', 18), yscrollcommand=vbar.set)
        self.tag_config("cursor", background="yellow", foreground="black")
        self.tag_config("good", background="white", foreground="green")
        self.tag_config("bad", background="white", foreground="red")

        self.status = 'Welcome'
        self.texts = texts
        self.show()

        self.bind_all('<Key>', self.type)

    def show(self):
        self.config(state=tk.NORMAL)
        if self.status == "Welcome":
            self.insert(tk.END, "Welcome!")
        elif self.status == "Training":
            for text in self.texts:
                self.insert(tk.END, text)
                self.insert(tk.END, '\u00B6\n')
            self.mark_set("cursor_mark", "0.0")
            self.mark_set("good_mark", "0.0")
            self.tag_add("cursor", "cursor_mark")
        elif self.status == "Summary":
            self.insert(tk.END, "Congratulations!")
        self.config(state=tk.DISABLED)

    def change_status(self):
        self.config(state=tk.NORMAL)
        self.delete("0.0", tk.END)
        if self.status == "Welcome":
            self.status = "Training"
        elif self.status == "Training":
            self.status = "Summary"
        elif self.status == "Summary":
            self.status = "Training"
        self.show()

    def get_type_char(self, event):
        key = event.keysym
        if key in LETTERS: return key
        if key in SPECIAL_KEYS: return SPECIAL_KEYS[key]
        if key == 'BackSpace': return -1
        if key == 'Return': return "newline"
        return
    def type(self, event):
        if self.status == 'Training':
            key = self.get_type_char(event)
            cursor_char = self.get(self.tag_ranges('cursor')[0], self.tag_ranges('cursor')[1])
            if key:
                move_good = (key==cursor_char or (key=="newline" and cursor_char=='\u00B6') or key==-1)
                self.remove_tags()
                self.update_marks(forward=(key!=-1), move_good=move_good)
                self.add_tags()
            if self.check_finish():
                self.change_status()
        else:
            self.change_status()

    def update_marks(self, forward=True, move_good=True):
        if move_good and self.compare('cursor_mark', '==', 'good_mark'):
            self.move_mark('good_mark', forward)
        self.move_mark('cursor_mark', forward)
    def move_mark(self, mark_name, forward):
        line, column = tuple(map(int, str.split(self.index(mark_name), ".")))
        if forward:
            step = 1
            if self.index("%d.end" % (line)) == ("%d.%d" % (line, column+1)):  # EOL
                line += 1
                column = -step
        else:
            step = -1
            if column == 0 and line > 1:  ## First line character
                line, column = tuple(map(int, str.split(self.index("%d.end" % (line-1)), ".")))
        self.mark_set(mark_name, "%d.%d" % (line, column + step))

    def remove_tags(self):
        self.tag_remove("good", "0.0", "good_mark")
        self.tag_remove("bad", 'good_mark', 'cursor_mark')
        self.tag_remove("cursor", "cursor_mark")
    def add_tags(self):
        self.tag_add("good", "0.0", 'good_mark')
        self.tag_add("bad", 'good_mark', 'cursor_mark')
        self.tag_add("cursor", "cursor_mark")

    def check_finish(self):
        line, column = tuple(map(int, str.split(self.index('good_mark'), ".")))
        end_line, end_column = tuple(map(int, str.split(self.index(tk.END), ".")))
        if line+1 == end_line and column == end_column:
            return True
        else: return False


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
# train_text1 = "A general theory of cookies may be formulated this way. Despite its descent from cakes and other sweetened breads, the cookie in almost all its forms has abandoned water as a medium for cohesion. Water in cakes serves to make the base (in the case of cakes called batter) as thin as possible, which allows the bubbles - responsible for a cake's fluffiness - to better form. In the cookie, the agent of cohesion has become some form of oil."
train_text1 = "A ge."
train_text2 = "A general theory of cookies may be formulated this way."
train_texts = [train_text1, train_text2]
# Define text box with scrollbar
vbar = tk.Scrollbar(top_frame,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)

train = TrainText(top_frame, train_texts)
train.pack(expand=True, fill="both")
vbar.config(command=train.yview)
# Mainloop
root.mainloop()
