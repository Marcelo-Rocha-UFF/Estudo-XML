from tkinter import *

# Let's create the Tkinter window
window = Tk()
window.title("Eva Emulator v 1.0")
window.geometry("838x525")


terminal = Text ( window, fg="yellow", bg="black", height="32", width="60")

Font_tuple = ("DejaVu Sans Mono", 9)
terminal.configure(font = Font_tuple)


# In order to display the image in a GUI, you will use the 'PhotoImage' method of Tkinter. It will an image from the directory (specified path) and store the image in a variable.
eva_image = PhotoImage(file = "eva.png")
bulb_image = PhotoImage(file = "bulb.png")

# Finally, to display the image you will make use of the 'Label' method and pass the 'image' variriable as a parameter and use the pack() method to display inside the GUI.
l_eva = Label(window, image = eva_image)
l_bulb = Label(window, image = bulb_image)
b_power = Button ( window, text="Power On")
b_import = Button ( window, text="Import Script File...")

terminal.insert(INSERT, "Eva emulator version 1.0 - UFF/MidiaCom\n")
terminal.insert(INSERT, "-----------------------------------------\n\n")
terminal.insert(INSERT, "Turn on the Robot, import a Script file and have fun!")
#label.pack()
l_eva.place(x=0, y=50)
l_bulb.place(x=290, y=200)
terminal.place(x=400, y=60)
b_power.place(x=470, y=20)
b_import.place(x=580, y=20)

window.mainloop()