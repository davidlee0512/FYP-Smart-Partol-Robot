from tkinter import * 
from tkinter import ttk
from ttkthemes import themed_tk 
from ttkthemes import ThemedTk
linenum = 0
root = ThemedTk(theme="radiance") 
root.title('Q&A Chatbot')
root.geometry("400x400")
root.resizable(0, 0) 
frame1 = LabelFrame(root,borderwidth = 0, highlightthickness = 0,width=250) 
frame2 = LabelFrame(root,borderwidth = 0, highlightthickness = 0,width=250)
inputbox = ttk.Entry(frame2, width=30)
inputbox.grid(row=0, column=0)
inputbox.insert(0, "Type in your question here")
frame1.place(x=20, y=0)
frame2.place(x=20, y=370)
def on_click(event):
    if inputbox.get() =="Type in your question here" :
        event.widget.delete(0, END)

def ask(event=None):
    global linenum
    if linenum>16 :
        for widget in frame1.winfo_children():
            widget.destroy()
        linenum=1
    if inputbox.get() !="" :
        question = inputbox.get()
        mylable= ttk.Label(frame1, text=question,anchor='w',width = 45,wraplengt=350, background='#BC986A', foreground='White',font=('Helvetica', 11))
        mylable.grid(row=linenum, column=0,padx=0)
        linenum = linenum + 1
        mylable2= ttk.Label(frame1, text="ANSWER",anchor='e',width = 45,background='#FBEEC1',font=('Helvetica', 11))
        mylable2.grid(row=linenum, column=0,padx=0)
        answerlength = 1
        linenum = linenum + answerlength
        inputbox.delete(0,END)

inputbox.bind('<Return>', ask)
inputbox.bind("<Button-1>", on_click)
askbutton = ttk.Button(frame2, text="Ask Question", command=lambda: ask(),width=13)
askbutton.grid(row=0, column=1, padx=30)

root.mainloop()