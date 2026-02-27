import tkinter as tk

root = tk.Tk()
root.title("Tester reakční doby")

frame = tk.Frame(root, padding=10)
frame.grid()
tk.Label(frame, text="Hello World!").grid(column=0, row=0)
tk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)

root.mainloop()
