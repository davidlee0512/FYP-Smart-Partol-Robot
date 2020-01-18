from tkinter import * 
from tkinter import ttk
from ttkthemes import themed_tk 
from ttkthemes import ThemedTk
import tkinter as tk
import time
from chatbot import Chatbot

chatbot = Chatbot(categorys = ["restaurant", "shop", "facility"], dbargs = ("localhost", "root", "Davidlee12059801", "airport_info"))
linenum = 0
root = ThemedTk(theme="radiance") 
root.title('Q&A Chatbot')
root.geometry("400x300")
root.resizable(0, 0) 

container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
frame2 = LabelFrame(root,borderwidth = 0, highlightthickness = 0,width=250)
inputbox = ttk.Entry(frame2, width=30)
inputbox.grid(row=0, column=0)
inputbox.insert(0, "Type in your question here")
frame2.place(x=20, y=270)
def on_click(event):
    canvas.yview_moveto(1)
    if inputbox.get() =="Type in your question here" :
        event.widget.delete(0, END)

def ask(event=None):
    global linenum
    if inputbox.get() !="" :
        question = inputbox.get()
        mylable= ttk.Label(scrollable_frame, text=question,anchor='w',width = 45,wraplengt=350, background='#BC986A', foreground='White',font=('Helvetica', 11))
        mylable.grid(row=linenum, column=0,padx=0)
        linenum = linenum + 1
        mylable2= ttk.Label(scrollable_frame, text=answer,anchor='e',width = 45,background='#FBEEC1',font=('Helvetica', 11))
        answer = chatbot.askQuestion(question)
        mylable2.grid(row=linenum, column=0,padx=0)
        answerlength = answer.count("\n") + 1
        linenum = linenum + answerlength
        inputbox.delete(0,END)
        canvas.yview_moveto(1)
        toend()
    if inputbox.get() =="":
        toend()
        canvas.yview_moveto(1)
def toend():
    canvas.yview_moveto(1)



inputbox.bind('<Return>', ask)
inputbox.bind("<Button-1>", on_click)
askbutton = ttk.Button(frame2, text="Ask Question", command=lambda: [ask(),toend()],width=13)
askbutton.grid(row=0, column=1, padx=30)

root.mainloop()