from tkinter import * 
root = Tk()

inputbox = Entry(root, width=50)
inputbox.pack()
inputbox.insert(0, "Type in your question here")


def on_click(event):
    event.widget.delete(0, END)

def ask():
    question = inputbox.get()
    mylable= Label(root, text=question)
    mylable.pack()
    inputbox.delete(0,END)

inputbox.bind("<Button-1>", on_click)
askbutton = Button(root, text="Ask Question", command=ask)
askbutton.pack()

root.mainloop()