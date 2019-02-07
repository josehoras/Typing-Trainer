import tkinter as tk
from six.moves import cPickle as pickle
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import datetime
import wikipedia
import random
import time

matplotlib.use('TkAgg')

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
    forms = ['Sr', 'Jr']
    if f_sent_l_word in forms or len(f_sent_l_word) == 1:
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
        super().__init__(frame, wrap=tk.WORD, bg="white smoke", height=20, width=70,
                         font=('monospace', 14), yscrollcommand=vbar.set,
                         spacing1=2, padx=5, pady=10, borderwidth=4)

        self.tag_config("good", background="white smoke", foreground="green")
        self.tag_config("bad", background="misty rose", foreground="red")
        self.tag_config("corrected", background="gainsboro", foreground="gold4")
        self.tag_config("cursor", background="yellow", foreground="black")
        self.bad = set()
        self.corrected = set()

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
            self.bad = set()
            self.corrected = set()
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
                if move_good and key!=-1 and self.index('cursor_mark') in self.bad:
                    self.bad.remove(self.index('cursor_mark'))
                    self.corrected.add(self.index('cursor_mark'))
                if not move_good or self.compare('cursor_mark', '!=', 'good_mark') and key!=-1:
                    self.mistakes += 1
                    self.bad.add(self.index('cursor_mark'))
                self.remove_tags()
                self.update_marks(forward=(key!=-1), move_good=move_good)
                self.add_tags()
            if self.check_finish():
                self.change_status()
            self.check_and_scroll()
        else:
            self.change_status()
    def check_and_scroll(self):
        cursor_y = self.dlineinfo('cursor_mark')[1]
        window_height = self.winfo_height()
        if cursor_y + 30 > window_height:
            self.yview_scroll(window_height/2, 'pixels')

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
        self.tag_remove("cursor", "cursor_mark")
        for m in self.bad:
            self.tag_remove('bad', m)
        for c in self.corrected:
            self.tag_remove('corrected', c)

    def add_tags(self):
        self.tag_add("good", "0.0", 'good_mark')
        self.tag_add("cursor", "cursor_mark")
        for m in self.bad:
            self.tag_add('bad', m)
        for c in self.corrected:
            self.tag_add('corrected', c)

    def check_finish(self):
        line, column = tuple(map(int, str.split(self.index('good_mark'), ".")))
        end_line, end_column = tuple(map(int, str.split(self.index(tk.END), ".")))
        if line+1 == end_line and column == end_column:
            return True
        else: return False

    def save_progress(self, wpm, acc, score):
        max_length = int(max_word_text.bmax_words.get())
        date = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
        try:
            wpm_series, acc_series, score_series, date_series = \
                pickle.load(open(PROGRESS_FILE, 'rb'), encoding='latin1')
        except (OSError, IOError):  # No progress file yet available
            wpm_series = {100:[], 200:[], 300:[], 400:[], 500:[]}
            acc_series = {100:[], 200:[], 300:[], 400:[], 500:[]}
            score_series = {100:[], 200:[], 300:[], 400:[], 500:[]}
            date_series = {100:[], 200:[], 300:[], 400:[], 500:[]}
        wpm_series[max_length].append(wpm)
        acc_series[max_length].append(acc)
        score_series[max_length].append(score)
        date_series[max_length].append(date)
        pickle.dump([wpm_series, acc_series, score_series, date_series], open(PROGRESS_FILE, 'wb'))

    def get_wiki_text(self):
        max_length = int(max_word_text.bmax_words.get())
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


class WordMaxInput():
    # Create max words list
    def __init__(self, parent):
        w = tk.Label(parent, text="Max. words: ", font=10)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        var = tk.StringVar()
        self.bmax_words = tk.Spinbox(parent, values=(100, 200, 300, 400, 500), textvariable=var,
                                bg="white", width=5, justify=tk.CENTER, state='readonly')
        var.set(300)  # default value
        self.bmax_words.pack(side=tk.LEFT, padx=0, pady=5)


class ProgressPlotsWindow(tk.Tk):
    def __init__(self, p):
        super().__init__()
        self.title("Progress")
        self.top_frame = tk.Frame(self,width=100,height=100)
        self.top_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.bottom_frame = tk.Frame(self,width=100,height=100)
        self.bottom_frame.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH)
        self.b_score = tk.Button(self.top_frame, text='Score', font=10, command=p.plot_score)
        self.b_score.pack(side=tk.RIGHT, padx=5, pady=5)
        self.b_acc = tk.Button(self.top_frame, text='Accuracy', font=10, command=p.plot_acc)
        self.b_acc.pack(side=tk.RIGHT, padx=5, pady=5)
        self.b_wpm = tk.Button(self.top_frame, text='Words per minute', font=10, command=p.plot_wpm)
        self.b_wpm.pack(side=tk.RIGHT, padx=5, pady=5)
        self.max_word_plot = WordMaxInput(self.top_frame)
        self.fig = plt.figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.bottom_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

class ProgressPlots():
    def __init__(self):
        try:
            self.wpm_series, self.acc_series, self.score_series, self.date_series = \
                pickle.load(open(PROGRESS_FILE, 'rb'), encoding='latin1')
        except (OSError, IOError):  # No progress file yet available
            self.wpm_series = {100:[], 200:[], 300:[], 400:[], 500:[]}
            self.acc_series = {100:[], 200:[], 300:[], 400:[], 500:[]}
            self.score_series = {100:[], 200:[], 300:[], 400:[], 500:[]}
            self.date_series = {100: [], 200: [], 300: [], 400: [], 500: []}
        self.window = ProgressPlotsWindow(self)

    def plot_wpm(self):
        max_length = int(self.window.max_word_plot.bmax_words.get())
        dates = [datetime.datetime.strptime(d, '%Y-%m-%d %H:%M') for d in self.date_series[max_length]]
        dates_f = [d.strftime('%d %b %y, %H:%M') for d in dates]
        plt.cla()
        plt.title("Words per minute")
        plt.scatter(dates_f, self.wpm_series[max_length])
        plt.plot(dates_f, self.wpm_series[max_length])
        plt.gcf().subplots_adjust(bottom=0.25, left=0.2)
        plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.ylim(0, 60)
        self.window.canvas.draw()
    def plot_acc(self):
        max_length = int(self.window.max_word_plot.bmax_words.get())
        dates = [datetime.datetime.strptime(d, '%Y-%m-%d %H:%M') for d in self.date_series[max_length]]
        dates_f = [d.strftime('%d %b %y, %H:%M') for d in dates]
        plt.cla()
        plt.title("Accuracy")
        plt.scatter(dates_f, self.acc_series[max_length])
        plt.plot(dates_f, self.acc_series[max_length])
        plt.gcf().subplots_adjust(bottom=0.25, left=0.2)
        plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.yticks=(80, 90, 100)
        plt.ylim(80, 100)
        self.window.canvas.draw()
    def plot_score(self):
        max_length = int(self.window.max_word_plot.bmax_words.get())
        dates = [datetime.datetime.strptime(d, '%Y-%m-%d %H:%M') for d in self.date_series[max_length]]
        dates_f = [d.strftime('%d %b %y, %H:%M') for d in dates]
        plt.cla()
        plt.title("Score")
        plt.scatter(dates_f, self.score_series[max_length])
        plt.plot(dates_f, self.score_series[max_length])
        plt.gcf().subplots_adjust(bottom=0.25, left=0.2)
        plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.ylim(0, 10)
        self.window.canvas.draw()


def start_plots():
    ProgressPlots().plot_wpm()

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
top_frame = tk.Frame(root,width=100,height=100)
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
bt.pack(side=tk.RIGHT, padx=10, pady=5)
# Create show progress button

bprogress = tk.Button(bottom_frame, text='Progress', font=10, command=start_plots)
bprogress.pack(side=tk.LEFT, padx=10, pady=5)
# Create reload text button
breload = tk.Button(bottom_frame, text='Reload Text', font=10, command=train.reload_text)
breload.pack(side=tk.LEFT, padx=10, pady=5)

max_word_text = WordMaxInput(top_frame)

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
print(time.strftime("%Y-%m-%d %H:%M", time.gmtime()))
root.mainloop()
