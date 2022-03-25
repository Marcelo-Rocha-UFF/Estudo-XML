import tkinter as tk

root = tk.Tk()
root.attributes('-fullscreen', True) # make main window full-screen

canvas = tk.Canvas(root, bg='white', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True) # configure canvas to occupy the whole main window

root.mainloop()