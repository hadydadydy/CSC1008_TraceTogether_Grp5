#original copy at 4.02pm
import tkinter as tk
from tkinter import *
import os 
from pathlib import Path

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        
        self.button1 = tk.Button(self)
        self.button1["text"] = "Show Close Contact List"
        self.button1["command"] = self.openExcel
        self.button1.pack(side="top")

        self.button2 = tk.Button(self)
        self.button2["text"] = "Show Cluster"
        self.button2["command"] = self.say_hi
        self.button2.pack(side="top")
        
        self.button3 = tk.Button(self)
        self.button3["text"] = "Show Safe Entry List"
        self.button3["command"] = self.say_hi
        self.button3.pack(side="top") 
        
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")
        
    def openExcel(self):
        absolutePath = Path('C:/Users/Public/src/dataset.xlsx').resolve()
        os.system(f'start excel.exe "{absolutePath}"')

root = tk.Tk()
root.title("Trace Together GUI ;-)")
root.geometry("300x300+10+10")
Application(master=root).mainloop()
