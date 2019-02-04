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
        super().__init__(frame, wrap=tk.WORD, bg="white", height=10, width=60,
                         font=('monospace', 14), yscrollcommand=vbar.set)
        self.tag_config("cursor", background="yellow", foreground="black")
        self.tag_config("good", background="white", foreground="green")
        self.tag_config("bad", background="lavender blush", foreground="red")

        self.start = 0
        self.finish_time = 0
        self.screens = ['Welcome', 'Training', 'Summary']
        self.status = 'Welcome'
        self.texts = texts
        self.characters = 0
        self.words = 0
        self.mistakes = 0
        self.show()
        # self.save_progress(1.5, 2, 0.5)
        # self.show_progress()
        self.bind_all('<Key>', self.type)

    def show(self):
        self.config(state=tk.NORMAL)
        if self.status == "Welcome":
            self.insert(tk.END, "Welcome!\n\n")
            self.insert(tk.END, "Press any key to start the exercise.")
        elif self.status == "Training":
            self.characters = 0
            self.words = 0
            self.mistakes = 0
            text = self.get_wiki_text()
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
            self.save_progress(wpm, acc, score)
            for line in summary:
                self.insert(tk.END, line)
        self.config(state=tk.DISABLED)

    def change_status(self):
        self.config(state=tk.NORMAL)
        self.delete("0.0", tk.END)
        if self.status == "Welcome":
            self.status = "Training"
        elif self.status == "Training":
            self.status = "Summary"
            self.finish_time = time.time() - self.start
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
        wiki_list = wikipedia.page("Wikipedia:Featured articles").links
        pagina = wikipedia.page(random.choice(wiki_list))
        text = pagina.summary
        if text.split('.')[0][-2:] == "Sr": i = 1
        else: i = 0
        check_brackets = text.split('.')[i]
        if '(' and ')' in check_brackets:
            a = check_brackets.index('(')
            b = check_brackets.index(')')
            in_brackets = check_brackets[a - 1:b + 1]
            no_brackets = check_brackets.replace(in_brackets, '')
            text = text.replace(check_brackets, no_brackets)
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
# Create show progress button
bprogress = tk.Button(bottom_frame, text='Progress', command=plot_progress)
bprogress.pack(side=tk.BOTTOM)
bprogress.pack(side=tk.LEFT, padx=10, pady=5)
# Define train text
train_text1 = "A general theory of cookies may be formulated this way. Despite its descent from cakes and other sweetened breads, the cookie in almost all its forms has abandoned water as a medium for cohesion. Water in cakes serves to make the base (in the case of cakes called batter) as thin as possible, which allows the bubbles - responsible for a cake's fluffiness - to better form. In the cookie, the agent of cohesion has become some form of oil."
train_text2 = "A general theory of cookies may be formulated this way."
train_texts = [train_text1]

# Define text box with scrollbar
vbar = tk.Scrollbar(top_frame,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)

train = TrainText(top_frame, train_texts)
train.pack(expand=True, fill="both")
vbar.config(command=train.yview)
# Mainloop
root.mainloop()
