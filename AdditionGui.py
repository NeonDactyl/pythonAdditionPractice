from tkinter import Tk, Label, Frame, Entry, N, E, S, W, StringVar, RIGHT
from random import choice
from datetime import datetime
import json
import threading
import sys
import os


class AdditionGui(object):
    def isCorrect(self):
        try:
            i = int(self.user_input.get())
            s = int(self.first.get()) + int(self.second.get())
            return i == s
        except ValueError:
            pass

    def resetCorrect(self):
        self.correct.set('')
        self.main_frame.config(bg=self.default_bg)
        for item in self.main_frame.winfo_children():
            if isinstance(item, Label):
                item.config(bg=self.default_bg)
        self.user_input.set('')
        self.problem = choice(self.problems)
        self.setProblem()

    def checkAnswer(self, *args):
        self.timer.cancel()
        del(self.timer)
        if self.isCorrect():
            self.main_frame.config(bg="green")
            for item in self.main_frame.winfo_children():
                if isinstance(item, Label):
                    item.config(bg="green")
            self.correct.set('Right! Good job!')
            self.right[self.prob_str] = self.right.get(self.prob_str, 0) + 1
        else:
            self.main_frame.config(bg="red")
            for item in self.main_frame.winfo_children():
                if isinstance(item, Label):
                    item.config(bg="red")
            self.correct.set('Nope, the answer is {}.'.format(self.answer))
            self.wrong[self.prob_str] = self.wrong.get(self.prob_str, 0) + 1
        self.timer = threading.Timer(1.0, self.resetCorrect)
        self.timer.start()

    def loadPrevious(self):
        try:
            pathname = os.path.abspath(os.path.dirname(sys.argv[0]))
            f = open(pathname + "\\data.json", "r")
            self.previous_results = json.load(f)
            f.close()
        except FileNotFoundError:
            self.previous_results = {}

    def saveResults(self):
        self.previous_results[self.TIME_KEY] = {}
        self.previous_results[self.TIME_KEY]["right"] = self.right
        self.previous_results[self.TIME_KEY]["wrong"] = self.wrong
        pathname = os.path.abspath(os.path.dirname(sys.argv[0]))
        with open(pathname + "\\data.json", "w") as f:
            json.dump(self.previous_results, f, indent=4)

    def generateProblems(self):
        self.problems = []
        for first in range(0, 10):
            for second in range(0, 11-first):
                r = 1
                w = 2
                p = str((first, second))
                for k in self.previous_results.keys():
                    r += self.previous_results[k]["right"].get(p, 0)
                    w += self.previous_results[k]["wrong"].get(p, 0)
                weight = (100 * w) // (r + w)
                self.problems.extend([(first, second)] * weight)

    def setProblem(self):
        self.first.set(self.problem[0])
        self.second.set(self.problem[1])
        self.answer = self.problem[0] + self.problem[1]
        self.prob_str = str(self.problem)

    def onClose(self):
        self.saveResults()
        self.timer.cancel()
        self.root.destroy()

    def setFont(self, l):
        l.config(font=("Helvetica", 36))

    def __init__(self):
        self.root = Tk()
        self.root.title("Addition Practice")
        self.loadPrevious()
        self.generateProblems()
        self.TIME_KEY = str(datetime.now())
        self.right = {}
        self.wrong = {}
        self.timer = threading.Timer(1.0, self.resetCorrect)

        self.main_frame = Frame(self.root)
        self.main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.user_input = StringVar()
        self.first = StringVar()
        self.second = StringVar()
        self.correct = StringVar()
        self.correct.set('')

        self.first_label = Label(self.main_frame, textvariable=self.first)
        self.first_label.grid(column=1, row=0, sticky=(N, W, E))
        self.setFont(self.first_label)

        self.plus_label = Label(self.main_frame, text="+")
        self.plus_label.grid(column=0, row=1, sticky=(E, N, S))
        self.setFont(self.plus_label)

        self.second_label = Label(self.main_frame, textvariable=self.second)
        self.second_label.grid(column=1, row=1, sticky=(W, E, S, N))
        self.setFont(self.second_label)

        self.user_input_entry = Entry(self.main_frame, width=7,
                                      textvariable=self.user_input, justify=RIGHT)
        self.user_input_entry.grid(column=0, row=2, columnspan=2, sticky=(N))
        self.setFont(self.user_input_entry)

        self.correct_label = Label(self.main_frame, textvariable=self.correct)
        self.correct_label.grid(column=0, row=3, columnspan=2, sticky=(W, E, S))
        self.correct_label.config(font=("Helvetica", 24), wraplength=250)

        self.default_bg = self.root.cget('bg')

        for child in self.main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for i in range(2):
            self.main_frame.columnconfigure(i, weight=1)
        for i in range(2, 4):
            self.main_frame.rowconfigure(i, weight=1)

        self.user_input_entry.focus()
        self.root.bind('<Return>', self.checkAnswer)
        self.problem = choice(self.problems)
        self.setProblem()
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.root.resizable(False, False)
        self.root.geometry("300x300")
        self.root.mainloop()


if __name__ == '__main__':
    gui = AdditionGui()
