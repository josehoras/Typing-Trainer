import tkinter as tk
from six.moves import cPickle as pickle
import matplotlib.pyplot as plt
import wikipedia
import random
import time

PROGRESS_FILE = "progress.p"
LETTERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
           'q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p',
           'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
           'y', 'x', 'c', 'v', 'b', 'n', 'm',
           'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P',
           'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
           'Y', 'X', 'C', 'V', 'B', 'N', 'M']
SPECIAL_KEYS = {'degree': '°', 'asciicircum': '^', 'exclam': '!', 'quotedbl': '"',
                'section': '§', 'dollar': '$', 'percent': '%', 'ampersand': "&", 'slash': "/",
                'parenleft': '(', 'parenright': ')', 'equal': '=', 'question': '?',
                'grave': '`', 'space': " ", 'ssharp': "ß", 'acute': '´', 'plus': '+',
                'less': '<', 'comma': ',', 'period': '.', 'minus': '-', 'underscore': '_',
                'udiaeresis': 'ü', 'Udiaeresis': 'Ü', 'odiaeresis': 'ö', 'Odiaeresis': 'Ö',
                'adiaeresis': 'ä', 'Adiaeresis': 'Ä', 'asterisk': '*', 'numbersign': '#',
                'apostrophe': "'", 'colon': ':', 'semicolon': ';', 'greater': '>', 'at': '@'}

def format(txt):
    f_sent_l_word = txt.split('.')[0].split()[-1]
    print(f_sent_l_word)
    # Remove brakets in first sentence, that often includes non keyboard characters
    if f_sent_l_word == "Sr" or len(f_sent_l_word) == 1:
        i = 1
    else:
        i = 0
    check_brackets = txt.split('.')[i]
    if '(' and ')' in check_brackets:
        a = check_brackets.index('(')
        b = check_brackets.index(')')
        in_brackets = check_brackets[a - 1:b + 1]
        no_brackets = check_brackets.replace(in_brackets, '')
        txt = txt.replace(check_brackets, no_brackets)
    ntext = txt
    h = 0
    for i in range(len(txt)):
        if txt[i] == "\n":
            ntext = ntext[:i+h] + "\u00B6" + ntext[i+h:]
            h += 1
        if txt[i] == "–" or txt[i] == "—":
            ntext = ntext[:i+h] + "-" + ntext[i+h+1:]
    return ntext


class TrainText(tk.Text):
    def __init__(self, frame, texts=[]):
        super().__init__(frame, wrap=tk.WORD, bg="white", height=20, width=70,
                         font=('monospace', 14), yscrollcommand=vbar.set)
        self.tag_config("cursor", background="yellow", foreground="black")
        self.tag_config("good", background="white", foreground="green")
        self.tag_config("bad", background="lavender blush", foreground="red")

        self.start = 0
        self.finish_time = 0
        self.screens = ['Welcome', 'Loading', 'Training', 'Summary']
        self.status = 'Welcome'
        self.texts = texts
        self.characters = 0
        self.words = 0
        self.mistakes = 0
        self.show()
        self.bind_all('<Key>', self.type)

    def show(self):
        self.config(state=tk.NORMAL)

        if self.status == "Welcome":
            self.insert(tk.END, "Welcome!\n\n")
            self.insert(tk.END, "Press any key to load the next text.")
        elif self.status == "Loading":
            self.insert(tk.END, "Loading Wikipedia page...")
            root.update()
            self.text = self.get_wiki_text()
            self.insert(tk.END, "\n\nPress any key to start the exercise.")
        elif self.status == "Training":
            self.characters = 0
            self.words = 0
            self.mistakes = 0
            text = self.text
            # for text in self.texts:
            self.characters += len(text)
            self.words += len(text.split())
            self.insert(tk.END, text)
            self.insert(tk.END, '\u00B6\n')
            self.mark_set("cursor_mark", "0.0")
            self.mark_set("good_mark", "0.0")
            self.tag_add("cursor", "cursor_mark")
            self.start = time.time()
        elif self.status == "Summary":
            word_count_var.set(0)
            min = int(self.finish_time / 60)
            sec = self.finish_time % 60
            cps = self.characters / self.finish_time
            wpm = 60 * self.words / self.finish_time
            acc = 100 * (1 - self.mistakes / self.characters)
            score = 2 * cps * acc/100
            summary = []
            summary.append("Congratulations!\n")
            summary.append("You did it in %i minutes and %i seconds\n" % (min, sec))
            summary.append("Characters per second: %.1f\n" % cps)
            summary.append("Words per minute: %.1f\n" % wpm)
            summary.append("Accuracy: %.1f%%\n" % acc)
            summary.append("Score: %.2f\n" % score)
            summary.append("\nPress any key to continue training.")
            self.save_progress(wpm, acc, score)
            for line in summary:
                self.insert(tk.END, line)
        self.config(state=tk.DISABLED)

    def change_status(self):
        self.config(state=tk.NORMAL)
        self.delete("0.0", tk.END)
        if self.status == "Welcome":
            self.status = "Loading"
        elif self.status == "Loading":
            self.status = "Training"
        elif self.status == "Training":
            self.status = "Summary"
            self.finish_time = time.time() - self.start
        elif self.status == "Summary":
            self.status = "Loading"
        self.show()
    def reload_text(self):
        self.config(state=tk.NORMAL)
        self.delete("0.0", tk.END)
        self.status = "Loading"
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
                if not move_good: self.mistakes += 1
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

    def save_progress(self, wpm, acc, score):
        try:
            wpm_series, acc_series, score_series = pickle.load(open(PROGRESS_FILE, 'rb'), encoding='latin1')
            wpm_series.append(wpm)
            acc_series.append(acc)
            score_series.append(score)
            pickle.dump([wpm_series, acc_series, score_series], open(PROGRESS_FILE, 'wb'))
        except (OSError, IOError):  # No progress file yet available
            pickle.dump([[wpm], [acc], [score]], open(PROGRESS_FILE, 'wb'))

    def show_progress(self):
        try:
            wpm_series, acc_series, score_series = pickle.load(open(PROGRESS_FILE, 'rb'), encoding='latin1')
            print(wpm_series)
            print(acc_series)
            print(score_series)
        except (OSError, IOError):  # No progress file yet available
            print("No data")
    def get_wiki_text(self):
        max_length = int(bmax_words.get())
        wiki_list = wikipedia.page("Wikipedia:Featured articles").links
        go = 0
        while go==0:
            pagina = wikipedia.page(random.choice(wiki_list))
            text = pagina.summary
            print(len(text.split()), " ", int(max_length), " ")
            if len(text.split()) <= max_length and len(text.split()) > max_length/2:
                go = 1
            else:
                for i in reversed(range(1, len(text.split("\n")))):
                    print(i)
                    shorter_text = ''.join(text.split("\n")[0:i])
                    print(len(shorter_text.split()))
                    if len(shorter_text.split()) <= max_length and len(shorter_text.split()) > max_length/2:
                        text = shorter_text
                        go = 1
                        break
        text = format(text)
        word_count_var.set(len(text.split()))
        return text

# Finally not in the class
def plot_progress():
    try:
        wpm_series, acc_series, score_series = pickle.load(open(PROGRESS_FILE, 'rb'), encoding='latin1')
    except (OSError, IOError):  # No progress file yet available
        print("No data")
        return
    xs = [x for x in range(len(wpm_series))]
    plt.subplot(3, 1, 1)
    plt.title("Words per minute")
    plt.scatter(xs,wpm_series)
    plt.plot(xs,wpm_series)
    plt.ylim(0, 60)
    plt.setp(plt.gca(), xticklabels=[], xticks=[])#, yticks=(0, 90, 100))
    plt.subplot(3, 1, 2)
    plt.title("Accuracy")
    plt.scatter(xs,acc_series)
    plt.plot(xs,acc_series)
    plt.ylim(80, 100)
    plt.setp(plt.gca(), xticklabels=[], xticks=[], yticks=(80, 90, 100))
    plt.subplot(3, 1, 3)
    plt.title("Score")
    plt.scatter(xs,score_series)
    plt.plot(xs,score_series)
    plt.setp(plt.gca(), xticklabels=[], xticks=[])
    plt.show()

# Define train text
train_text1 = "A general theory of cookies may be formulated this way. Despite its descent from cakes and other sweetened breads, the cookie in almost all its forms has abandoned water as a medium for cohesion. Water in cakes serves to make the base (in the case of cakes called batter) as thin as possible, which allows the bubbles - responsible for a cake's fluffiness - to better form. In the cookie, the agent of cohesion has become some form of oil."
train_text2 = "A general theory of cookies may be formulated this way."
train_texts = [train_text1]
# Create main window
root = tk.Tk()
root.title("Typing Trainer")
root.minsize(70, 38)
# Create frames in window
bottom_frame = tk.Frame(root,width=100,height=100)
bottom_frame.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH)
top_frame = tk.Frame(root,width=800,height=700)
top_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
center_frame = tk.Frame(root,width=100,height=100)
center_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
# Define text box with scrollbar
vbar = tk.Scrollbar(center_frame,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)
train = TrainText(center_frame, train_texts)
train.pack(expand=True, fill="both")
vbar.config(command=train.yview)
# Create quit button
bt = tk.Button(bottom_frame, text='Quit', font=10, command=root.destroy)
bt.pack(side=tk.BOTTOM)
bt.pack(side=tk.RIGHT, padx=10, pady=5)
# Create show progress button
bprogress = tk.Button(bottom_frame, text='Progress', font=10, command=plot_progress)
# bprogress.pack(side=tk.BOTTOM)
bprogress.pack(side=tk.LEFT, padx=10, pady=5)
# Create reload text button
breload = tk.Button(bottom_frame, text='Reload Text', font=10, command=train.reload_text)
# breload.pack(side=tk.BOTTOM)
breload.pack(side=tk.LEFT, padx=10, pady=5)
# Create max words list
w = tk.Label(top_frame, text="Max. words: ", font=10)
w.pack(side=tk.LEFT, padx=5, pady=5)
var = tk.StringVar()
bmax_words = tk.Spinbox(top_frame, values=(100, 200, 300, 400, 500), textvariable=var,
                        bg="white", width=5, justify=tk.CENTER, state='readonly')
var.set(300) # default value
bmax_words.pack(side=tk.LEFT, padx=0, pady=5)
print(bmax_words.get())
# Create number of words label

word_count_var = tk.StringVar()
word_count_var.set(0)
lword_count = tk.Label(top_frame, textvariable=word_count_var, font=10)
lword_count.pack(side=tk.RIGHT, padx=5, pady=5)
lword_count_txt = tk.Label(top_frame, text="# of words: ", font=10)
lword_count_txt.pack(side=tk.RIGHT, padx=5, pady=5)
# from tkinter import font
# for f in set(font.families()):
#     print(f)
# Mainloop
root.mainloop()
