from tkinter import *
#from tkinter import messagebox

def myAction():
    myLabelAction = Label(app, text='Now action!').pack()


def mNew():
    myLabelAction = Label(app, text='Now action!').pack()
    return

def mAbout():
    messagebox.showinfo(title="About", message="This is my about box") 
    return

def mQuit():
    mExit = messagebox.askyesno(title="Quit?", message="Are you sure?")
    if (mExit > 0):
        app.destroy()
        return    

app = Tk()
app.title("Tkinter menu testprogram")
app.geometry("450x300+100+100")

labeltext = StringVar()
labeltext.set("Hello")
label1 = Label(app, textvariable=labeltext, height=4).pack()

myLabel2 = Label(app, text='Label2 her!').pack()

myButton = Button(app, text='OK', fg='red', bg='blue').pack()
myButton2 = Button(app, text='Action', command = myAction).pack()

#menu construction

menubar = Menu(app)

#File menu
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label="New", command = mNew)
filemenu.add_command(label="Exit", command = mQuit)
menubar.add_cascade(label="File", menu=filemenu)

#Help menu
helpmenu = Menu(menubar, tearoff = 0)
helpmenu.add_command(label="About", command = mAbout)
menubar.add_cascade(label="Help", menu=helpmenu)

app.config(menu=menubar)



app.mainloop()
