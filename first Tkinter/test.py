from tkinter import *

def myAction():
    myLabelAction = Label(app, text='Now action!').pack()

app = Tk()
app.title("XXX")
app.geometry("450x300+100+100")

labeltext = StringVar()
labeltext.set("Hello")
label1 = Label(app, textvariable=labeltext, height=4)
label1.pack()

myLabel2 = Label(app, text='Label2 her!').pack()

myButton = Button(app, text='OK', fg='red', bg='blue').pack()
myButton2 = Button(app, text='Action', command = myAction).pack()



app.mainloop()
