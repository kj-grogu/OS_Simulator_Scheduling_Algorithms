from tkinter import * #Tk, Button, Frame, Label, StringVar, OptionMenu
from tkinter import ttk
from ttkthemes import ThemedTk

def increase():
    value = int(label2["text"])
    label2["text"] = f"{value + 1}"
    value = int(label2["text"])
    label2["text"] = f"{value + 1}"
    value = int(label2["text"])
    label2["text"] = f"{value + 1}"

def decrease():
    value = int(label2["text"])
    label2["text"] = f"{value - 1}"

root = ThemedTk(theme='yaru')
root.geometry('800x800')
root.state('zoomed')# maximized
root.title('Operating System Simulator')


# divide the root into 3 rows and 1 col
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=3)
root.grid_rowconfigure(2, weight=1)


frame1 = Frame(root, background="Blue", height=5)
frame2 = Frame(root, background="Red")
frame3 = Frame(root, background="yellow")

frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=1, column=0, sticky="nsew")
frame3.grid(row=2, column=0, sticky="nsew")


# divide frame 3 into 1 row , 3 cols
frame1.grid_rowconfigure(0, weight=1)
frame1.grid_columnconfigure(0, weight=1)
frame1.grid_columnconfigure(1, weight=1)

frame1_1 = Frame(frame1, background="Blue")
frame1_1.grid(row = 0, column=1, sticky="nsew")
frame1_1.grid_rowconfigure(0, weight=1)
frame1_1.grid_columnconfigure(0, weight=1)
frame1_1.grid_columnconfigure(1, weight=1)


#
# label1_2 = Label(frame1,text='Label1_2',bg="white")
# label1_2.grid(row=0, column=1, sticky="nsew")

#
button1 = Button(
    master=frame1_1,
    text="Start",
    bg="black",
    fg="yellow",
    command=increase
)
button1.grid(row = 0, column = 0, sticky = "nsew")
button2 = Button(
    master=frame1_1,
    text="Stop",
    bg="black",
    fg="yellow",
    command=decrease
)
button2.grid(row = 0, column = 1, sticky = "nsew")

label2 = Label(frame2,text='0', bg="green")
label2.grid(row=0, column=0, sticky="nsew")

label3 = Label(frame3,text='Label3',bg="orange")
label3.grid(row=0, column=0, sticky="nsew")

options = ['winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative']

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set(options[0])

# Create Dropdown menu
drop = OptionMenu(frame1, clicked, *options)
drop.config(width=10, height=10)
drop.grid(row=0, column=0, sticky="nsew")





root.mainloop()