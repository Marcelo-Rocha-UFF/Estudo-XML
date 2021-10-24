# Import required libraries
from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame
win = Tk()

# Set the window size
win.geometry("700x350")
style = ttk.Style()
style.theme_use('clam')

# Define a function to implement choice function
def choice(option):
   pop.destroy()
   if option == "yes":
      label.config(text="Hello, How are You?")
   else:
      label.config(text="You have selected No")
      win.destroy()
def click_fun():
   global pop
   pop = Toplevel(win)
   pop.title("Confirmation")
   pop.geometry("300x150")
   #pop.config(bg="white")
   pop.grab_set()
   # Create a Label Text
   label = Label(pop, text="Would You like to Proceed?",
   font=('Aerial', 12))
   label.pack(pady=20)
   # Add a Frame
   frame = Frame(pop, bg="gray71")
   frame.pack(pady=10)
   # Add Button for making selection
   button1 = Button(frame, text="Yes", command=lambda: choice("yes"), bg="blue", fg="white")
   button1.grid(row=0, column=1)
   button2 = Button(frame, text="No", command=lambda: choice("no"), bg="blue", fg="white")
   button2.grid(row=0, column=2)
# Create a Label widget
label = Label(win, text="", font=('Aerial', 14))
label.pack(pady=40)

# Create a Tkinter button
ttk.Button(win, text="Click Here", command=click_fun).pack()

win.mainloop()