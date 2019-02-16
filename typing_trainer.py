import tkinter as tk
from six.moves import cPickle as pickle
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import datetime
import wikipedia
import random
import time
import webbrowser

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
                'apostrophe': "'", 'colon': ':', 'semicolon': ';', 'greater': '>', 'at': '@',
                'twosuperior':'²', 'threesuperior':'³', 'asciitilde':'~', 'mu':'µ', 'bar':'|',
                'EuroSign':'€', 'backslash':'\\'}


class MyFrame(tk.Frame):
    def __init__(self, top_window, location):
        super().__init__(top_window)
        self.pack(side=location, expand=False, fill=tk.BOTH)


class MyButton(tk.Button):
    def __init__(self, frame, location, txt, command):
        super().__init__(frame, text=txt, font=10, command=command)
        self.pack(side=location, padx=8, pady=5)


class WordLimit():
    # Create max words list
    def __init__(self, parent, default=300):
        w = tk.Label(parent, text="Max. words: ", font=10)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.var = tk.IntVar()
        self.value = tk.Spinbox(parent, values=(100, 200, 300, 400, 500), textvariable=self.var,
                                bg="white", width=5, justify=tk.CENTER, state='readonly')
        self.value.pack(side=tk.LEFT, padx=0, pady=5)
        self.var.set(default)  # default value


class WordCounter():
    def __init__(self, frame):
        # Create number of words label
        self.counter = tk.StringVar()
        self.counter.set(0)
        lword_count_txt = tk.Label(frame, text="# of words: ", font=10)
        lword_count = tk.Label(frame, textvariable=self.counter, font=10)
        lword_count.pack(side=tk.RIGHT, padx=5, pady=5)
        lword_count_txt.pack(side=tk.RIGHT, padx=5, pady=5)


class MyMainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Trainer")
        # Create frames in window
        bottom_frame = MyFrame(self, tk.BOTTOM)
        top_frame = MyFrame(self, tk.TOP)
        center_frame = MyFrame(self, tk.TOP)
        # Set max words and word counter
        self.max_words = WordLimit(top_frame)
        words = WordCounter(top_frame)
        # Define text box with scrollbar
        txt_box = TrainText(center_frame, self.max_words.value, words.counter)
        # Create buttons
        MyButton(bottom_frame, tk.RIGHT, 'Quit', self.quit)
        MyButton(bottom_frame, tk.LEFT, 'Progress', lambda: ProgressPlotsWindow(self))
        MyButton(bottom_frame, tk.LEFT, 'Reload Text', txt_box.reload_text)


class ProgressPlotsWindow(tk.Toplevel):
    def __init__(self, top):
        super().__init__(master=top)
        self.title("Progress")
        self.top_frame = MyFrame(self, tk.TOP)
        self.bottom_frame = MyFrame(self, tk.BOTTOM)
        self.fig = plt.figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.bottom_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.max_words = WordLimit(self.top_frame, top.max_words.value.get())
        self.max_words.value.bind('<ButtonRelease-1>', lambda event: self.on_release(event))
        self.plot_data = load_data()  # wpm, acc, score, date
        self.plots = {0:'Words per minute', 1:'Accuracy', 2:'Score'}
        self.ylims = {0:(0,50), 1: (90,100), 2:(0,10)}
        self.current_plot = 0
        self.b_score = MyButton(self.top_frame, tk.RIGHT, self.plots[2],
                                lambda: self.plot(2, self.get_set()))
        self.b_acc = MyButton(self.top_frame, tk.RIGHT, self.plots[1],
                              lambda: self.plot(1, self.get_set()))
        self.b_wpm = MyButton(self.top_frame, tk.RIGHT, self.plots[0],
                              lambda: self.plot(0, self.get_set()))

        self.plot(self.current_plot, self.get_set())

    def on_release(self, e):
        nset = self.get_set() + (2 * (e.y < 10) - 1) * 100
        cset = sorted((100, nset, 500))[1]
        self.plot(self.current_plot, cset)

    def get_set(self):
        return self.max_words.var.get()

    def plot(self, plot_nr, plot_set):
        self.current_plot = plot_nr
        xdata = self.plot_data[3][plot_set]
        ydata = self.plot_data[plot_nr][plot_set]
        dates = [datetime.datetime.strptime(d, '%Y-%m-%d %H:%M') for d in xdata]
        dates_f = [d.strftime('%d %b %y, %H:%M') for d in dates]
        plt.cla()
        plt.title(self.plots[plot_nr])
        plt.scatter(dates_f, ydata)
        plt.plot(dates_f, ydata)
        plt.gcf().subplots_adjust(bottom=0.25, left=0.2)
        plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.ylim(self.ylims[plot_nr])
        # plt.locator_params(axis='x', numticks=10)
        ticks = [x for x in range(0, len(dates_f), int(len(dates_f)/10)+1)]
        if ticks[-1] != (len(dates_f) - 1): ticks[-1] = (len(dates_f)-1)
        print(ticks, len(dates_f))
        plt.xticks(ticks)
        plt.grid(True, 'major', 'y', ls='--')
        plt.grid(True, 'major', 'x', ls=':', lw=0.3)
        self.canvas.draw()


class TrainText(tk.Text):
    def __init__(self, frame, max_words, word_counter):
        # Define and place objects
        vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        super().__init__(frame, wrap=tk.WORD, bg="white smoke", height=20, width=70,
                         font=('monospace', 14), yscrollcommand=vbar.set,
                         spacing1=2, padx=5, pady=10, borderwidth=4)
        vbar.config(command=self.yview)
        self.pack(expand=True, fill="both")
        # Define tags and marks
        self.tag_config("good", background="white smoke", foreground="green")
        self.tag_config("bad", background="misty rose", foreground="red")
        self.tag_config("corrected", background="gainsboro", foreground="gold4")
        self.tag_config("cursor", background="yellow", foreground="black")
        self.tag_config("hyper", foreground="blue", underline=1)
        self.bad = set()
        self.corrected = set()
        # Define bindings
        self.bind_all('<Key>', self.type)
        self.tag_bind("hyper", "<Enter>", self._enter)
        self.tag_bind("hyper", "<Leave>", self._leave)
        self.tag_bind("hyper", "<Button-1>", self._click)
        # Define screen variables
        self.screens = ['Welcome', 'Loading', 'Training', 'Summary']
        self.screen_ix = 0
        self.start_time = 0
        self.finish_time = 0
        # Define text variables
        self.text = ''
        self.link = ''
        self.characters = 0
        self.word_counter = word_counter
        self.mistakes = 0
        self.max_words = max_words
        # Start show :)
        self.show()

    def show(self):
        self.config(state=tk.NORMAL)
        self.delete("0.0", tk.END)
        screen = self.screens[self.screen_ix]
        if screen == "Welcome":
            self.insert(tk.END, "Welcome!\n\nPress any key to load the next text.\n")
        elif screen == "Loading":
            self.characters = 0
            self.word_counter.set(0)
            self.mistakes = 0
            self.insert(tk.END, "Loading Wikipedia page...")
            self.update()
            self.text, self.link = get_wiki_text(int(self.max_words.get()))
            self.characters = len(self.text)
            self.word_counter.set(len(self.text.split()))
            self.insert(tk.END, "\n\nPress any key to start the exercise.\n\n")
            # self.insert(tk.END, self.link.split('/')[-1], "hyper")
        elif screen == "Training":
            self.insert(tk.END, self.text)
            self.insert(tk.END, '\u00B6\n')
            self.mark_set("cursor_mark", "0.0")
            self.mark_set("good_mark", "0.0")
            self.tag_add("cursor", "cursor_mark")
            self.bad = set()
            self.corrected = set()
            self.start_time = time.time()
        elif screen == "Summary":
            self.finish_time = time.time() - self.start_time
            minutes = int(self.finish_time / 60)
            sec = self.finish_time % 60
            cps = self.characters / self.finish_time
            wpm = 60 * int(self.word_counter.get()) / self.finish_time
            acc = 100 * (1 - self.mistakes / self.characters)
            score = 2 * cps * acc/100
            summary = ["Congratulations!\n"]
            summary.append("You did it in %i minutes and %i seconds\n" % (minutes, sec))
            summary.append("Characters per second: %.1f\n" % cps)
            summary.append("Words per minute: %.1f\n" % wpm)
            summary.append("Accuracy: %.1f%%\n" % acc)
            summary.append("Score: %.2f\n" % score)
            summary.append("\nPress any key to continue training.\n\n")
            self.save_progress(wpm, acc, score)
            for line in summary:
                self.insert(tk.END, line)
            self.insert(tk.END, self.link.split('/')[-1], "hyper")
        self.config(state=tk.DISABLED)

    def _enter(self, event):
        self.config(cursor="hand2")

    def _leave(self, event):
        self.config(cursor="")

    def _click(self, event):
        webbrowser.open_new(self.link)
        print("click")


    def change_status(self):
        if self.screen_ix < 3:
            self.screen_ix += 1
        elif self.screen_ix == 3:
            self.screen_ix = 1
        self.show()

    def reload_text(self):
        self.screen_ix = 1
        self.show()

    @staticmethod
    def get_type_char(event):
        key = event.keysym
        print(key)
        if key in LETTERS: return key
        if key in SPECIAL_KEYS: return SPECIAL_KEYS[key]
        if key == 'BackSpace': return -1
        if key == 'Return': return "newline"
        return

    def type(self, event):
        if self.screen_ix == 2:
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
        if cursor_y + 50 > window_height:
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
            if column == 0 and line > 1:  # First line character
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
        wpm_series, acc_series, score_series, date_series = load_data()
        max_length = int(self.max_words.get())
        date = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
        wpm_series[max_length].append(wpm)
        acc_series[max_length].append(acc)
        score_series[max_length].append(score)
        date_series[max_length].append(date)
        pickle.dump([wpm_series, acc_series, score_series, date_series], open(PROGRESS_FILE, 'wb'))


def load_data():
    try:
        wpm_series, acc_series, score_series, date_series = \
            pickle.load(open(PROGRESS_FILE, 'rb'), encoding='latin1')
    except (OSError, IOError):  # No progress file yet available
        empty = {100:[], 200:[], 300:[], 400:[], 500:[]}
        wpm_series, acc_series, score_series, date_series = [empty] * 4
    return wpm_series, acc_series, score_series, date_series


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
    if '('  in check_brackets and ')' in check_brackets:
        a = check_brackets.index('(')
        b = check_brackets.index(')')
        in_brackets = check_brackets[a - 1:b + 1]
        no_brackets = check_brackets.replace(in_brackets, '')
        txt = txt.replace(check_brackets, no_brackets)
    ntext = txt
    h = 0
    for i in range(len(txt)):
        if txt[i] == "\n":
            ntext = ntext[:i + h] + "\u00B6" + ntext[i + h:]
            h += 1
        if txt[i] == "–" or txt[i] == "—":
            ntext = ntext[:i + h] + "-" + ntext[i + h + 1:]
    return ntext


def get_wiki_text(max_length):
    wiki_list = wikipedia.page("Wikipedia:Featured articles").links
    go = 0
    while go == 0:
        link = random.choice(wiki_list)
        pagina = wikipedia.page(link)
        text = pagina.summary
        print(len(text.split()), " ", int(max_length), " ")
        if max_length >= len(text.split()) > max_length / 1.8:
            text = format(text)
            chars = set(text)
            chars.discard('¶')
            chars.discard('\n')
            if all([char in LETTERS or char in list(SPECIAL_KEYS.values()) for char in chars]):
                go = 1
            else:
                print(chars)
                print([char in LETTERS or char in list(SPECIAL_KEYS.values()) for char in chars])
        else:
            for i in reversed(range(1, len(text.split("\n")))):
                print(i)
                shorter_text = ''.join(text.split("\n")[0:i])
                print(len(shorter_text.split()))
                if max_length >= len(shorter_text.split()) > max_length / 1.8:
                    text = format(shorter_text)
                    chars = set(text)
                    chars.discard('¶')
                    chars.discard('\n')
                    if all([char in LETTERS or char in list(SPECIAL_KEYS.values()) for char in chars]):
                        go = 1
                    else:
                        print(chars)
                        print([char in LETTERS or char in list(SPECIAL_KEYS.values()) for char in chars])
                    break
    return text, 'https://en.wikipedia.org/wiki/' + link


main = MyMainWindow()
main.mainloop()
print(time.strftime("%Y-%m-%d %H:%M", time.gmtime()))


# from tkinter import font
# for f in set(font.families()):
#     print(f)
# Mainloop

