import tkinter as tk


class TrainText(tk.Text):
    def __init__(self):
        super().__init__(top_frame, wrap=tk.WORD, bg="white", height=8, width=50,
                         font=('helvetica', 18), yscrollcommand=vbar.set)
        self.insert(tk.END, train_text)
        self.config(state=tk.DISABLED)

        self.tag_config("good", background="white", foreground="green")
        self.tag_config("cursor", background="yellow", foreground="black")
        self.mark_set("cursor_mark", "0.0")
        self.set_cursor()

        self.bind_all('<Key>', self.type)

    def type(self, event):
        key = self.get_type_char(event)
        cursor_char = self.get(self.tag_ranges('cursor')[0], self.tag_ranges('cursor')[1])
        if key==cursor_char:
            self.remove_cursor()
            self.move_cursor_mark()
            self.set_cursor()
            self.tag_add("good", 0.0, 'cursor_mark')

    def get_type_char(self, event):
        letters = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                   'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p',
                   'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
                   'y', 'x', 'c', 'v', 'b', 'n', 'm',
                   'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P',
                   'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                   'Y', 'X', 'C', 'V', 'B', 'N', 'M']
        special_keys = {'degree':'°', 'asciicircum':'^', 'exclam':'!', 'quotedbl':'"',
                        'section':'§', 'dollar':'$', 'percent':'%', 'ampersand':"&",
                        'slash':"/", 'parenleft':'(', 'parenright':')', 'slash':"/",
                        'parenleft':'(','parenright':')', 'equal':'=', 'question':'?',
                        'grave':'`', 'space':" ", 'ssharp':"ß", 'acute':'´', 'plus':'+',
                        'less':'<', 'comma':',', 'period':'.', 'minus':'-', 'underscore':'_',
                        'udiaeresis':'ü', 'Udiaeresis':'Ü', 'odiaeresis':'ö', 'Odiaeresis':'Ö',
                        'adiaeresis':'ä', 'Adiaeresis':'Ä', 'asterisk':'*', 'numbersign':'#',
                        'apostrophe':"'", 'colon':':', 'semicolon':';', 'greater':'>', 'at':'@'}
        key = event.keysym
        if key in letters: return key
        if key in special_keys: return special_keys[key]
        if key == 'Shift_R': return
        if key == 'Shift_L': return
        return

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
