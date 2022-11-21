from tkinter import Tk, Frame, Label
from tkinter import ttk


# def increase():
#     value = int(label1["text"])
#     label1["text"] = f"{value + 1}"
#     value = int(label1["text"])
#     label1["text"] = f"{value + 1}"
#     value = int(label1["text"])
#     label1["text"] = f"{value + 1}"
#
# def decrease():
#     value = int(label_a["text"])
#     label_a["text"] = f"{value - 1}"

root = Tk()
root.geometry('800x800')
root.state('zoomed')# maximized
root.title('Operating System Simulator')

# divide the root into 2 rows and 2 cols
root.grid_rowconfigure(0, weight=3)
root.grid_columnconfigure(0, weight=3)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

frame1 = Frame(root, background="Blue")
frame2 = Frame(root, background="Red")
frame3 = Frame(root, background="yellow")
frame4 = Frame(root, background="Black")

frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=1, sticky="nsew")
frame3.grid(row=1, column=0, sticky="nsew")
frame4.grid(row=1, column=1, sticky="nsew")


# divide frame 3 into 1 row , 3 cols
frame3.grid_rowconfigure(0, weight=1)
frame3.grid_columnconfigure(0, weight=1)
frame3.grid_columnconfigure(1, weight=1)
frame3.grid_columnconfigure(2, weight=1)


label1 = Label(frame3,text='Label1',bg="white")
label1.grid(row=0, column=0, sticky="nsew")

label2 = Label(frame3,text='Label2', bg="green")
label2.grid(row=0, column=1, sticky="nsew")

label3 = Label(frame3,text='Label3',bg="orange")
label3.grid(row=0, column=2, sticky="nsew")

# label4 = Label(frame1,text='Label4',bg="white")
# label4.grid(row=1, column=1, sticky="nsew")



# button1 = Tk.Button(
#     master=frame2,
#     text="Increase!",
#     bg="black",
#     fg="yellow",
#     command=increase
# )
#
# button2 = Tk.Button(
#     master=frame2,
#     text="Decrease!",
#     bg="black",
#     fg="yellow",
#     command=decrease
# )

style = ttk.Style(root)
print(style.theme_names())

style.theme_use('vista')
root.mainloop()