import tkinter as tk


def increase():
    value = int(label_a["text"])
    label_a["text"] = f"{value + 1}"

def decrease():
    value = int(label_a["text"])
    label_a["text"] = f"{value - 1}"

window = tk.Tk()
window.state('zoomed')# maximized

frame1 = tk.Frame(master=window, bg="red")
frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame2 = tk.Frame(master=window, bg="blue")
frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame1_1 = tk.Frame(master=frame1, bg="yellow")
frame1_1.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
frame1_2 = tk.Frame(master=frame1, bg="white")
frame1_2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)


frame1_3 = tk.Frame(master=frame1, bg="black")
frame1_3.pack(fill=tk.BOTH, side=tk.TOP, expand=True)



frame1_3_1 = tk.Frame(master=frame1_3, bg="cyan")
frame1_3_1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
label1_3_1 = tk.Label(master=frame1_3_1, text="Process 1", fg="white", bg = "cyan")
label1_3_1.pack(fill=tk.BOTH, side=tk.TOP)

frame1_3_2 = tk.Frame(master=frame1_3, bg="black")
frame1_3_2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
label1_3_2 = tk.Label(master=frame1_3_2, text="Process 2", fg="white", bg = "black")
label1_3_2.pack(fill=tk.BOTH, side=tk.TOP)

frame1_3_3 = tk.Frame(master=frame1_3, bg="cyan")
frame1_3_3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
label1_3_3 = tk.Label(master=frame1_3_3, text="Process 3", fg="white", bg = "cyan")
label1_3_3.pack(fill=tk.BOTH, side=tk.TOP)



label_a = tk.Label(master=frame2, text="0",
    fg="white",
    bg="red")

label_c = tk.Label(master=frame1_1, text="CPU HERE",
                   fg="white",
                   bg="green")

label_a.pack(fill=tk.BOTH, side=tk.TOP)

label_c.pack(fill=tk.BOTH, side=tk.TOP)
#
button1 = tk.Button(
    master=frame2,
    text="Increase!",
    bg="black",
    fg="yellow",
    command=increase
)
button1.pack(fill=tk.X, side=tk.BOTTOM)

button2 = tk.Button(
    master=frame2,
    text="Decrease!",
    bg="black",
    fg="yellow",
    command=decrease
)
button2.pack(fill=tk.X, side=tk.BOTTOM)


window.mainloop()