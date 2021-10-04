from tkinter import *
from tkinter import filedialog as fd
from playsound import playsound
import time
import threading
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# watson
apikey = "0UyIQDYcNO7SytoTLOE-hMRME8o7jeAxcD21Bcd7ZZ9E"
url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/5bd04cd8-cf86-4fbc-b76d-66ee10427604"

# setup watson service
authenticator = IAMAuthenticator(apikey)
# tts service
tts = TextToSpeechV1(authenticator = authenticator)
tts.set_service_url(url)

# Eva tts function
def evaTalk(eva_text):
    with open("my_sounds/tts.mp3", 'wb') as audio_file:
        res = tts.synthesize(eva_text, accept = "audio/mp3", voice = 'en-US_AllisonV3Voice').get_result()
        audio_file.write(res.content)
    playsound("my_sounds/tts.mp3", block = False)

# Let's create the Tkinter window
window = Tk()
window.title("Eva Simulator for EvaML (A XML Based Language) - Version 1.0 - UFF/MidiaCom Lab")
window.geometry("838x525")
canvas = Canvas(window, bg = "#d9d9d9", width = 838, height = 525) # o canvas e' necessario para usar imagens com transparencia
canvas.pack()

# Terminal text configuration
terminal = Text ( window, fg = "blue", bg = "white", height = "32", width = "60")
Font_tuple = ("DejaVu Sans Mono", 9)
terminal.configure(font = Font_tuple)



# In order to display the image in a GUI, you will use the 'PhotoImage' method of Tkinter. It will an image from the directory (specified path) and store the image in a variable.
eva_image = PhotoImage(file = "eva.png")
bulb_image = PhotoImage(file = "bulb.png")

# eva expressions images
im_eyes_neutral = PhotoImage(file = "eyes_neutral.png")
im_eyes_angry = PhotoImage(file = "eyes_angry.png")
im_eyes_sad = PhotoImage(file = "eyes_sad.png")
im_eyes_happy = PhotoImage(file = "eyes_happy.png")
im_eyes_on = PhotoImage(file = "eyes_on.png")

# matrix voice images
im_matrix_blue = PhotoImage(file = "matrix_blue.png")
im_matrix_green = PhotoImage(file = "matrix_green.png")
im_matrix_yellow = PhotoImage(file = "matrix_yellow.png")
im_matrix_white = PhotoImage(file = "matrix_white.png")
im_matrix_red = PhotoImage(file = "matrix_red.png")
im_matrix_grey = PhotoImage(file = "matrix_grey.png")

im_bt_play = PhotoImage(file = "bt_play.png")
im_bt_stop = PhotoImage(file = "bt_stop.png")

# Finally, to display the image you will make use of the 'Label' method and pass the 'image' variriable as a parameter and use the pack() method to display inside the GUI.
#l_eva = Label(canva, image = eva_image)
#l_bulb = Label(canva, image = bulb_image)
#l_angry_eyes = Label(canva, image = angry_image)
canvas.create_image(160, 262, image = eva_image)
canvas.create_image(340, 280, image = bulb_image)


# Eva initialization function
def evaInit():
    b_power['state'] = DISABLED
    b_import['state'] = NORMAL
    evaEmotion("power_on")
    playsound("my_sounds/power_on.mp3", block = True)
    time.sleep(1)
    terminal.insert(INSERT, "\nstate: Initializing.")
    time.sleep(1)
    terminal.insert(INSERT, "\nstate: Turning on the blue light.")
    light("blue", "on")
    time.sleep(1)
    evaMatrix("blue")
    terminal.insert(INSERT, "\nstate: Speaking a greeting text.")
    playsound("my_sounds/greetings.mp3", block = True)
    time.sleep(1)
    terminal.insert(INSERT, "\nstate: Turning off the light.")
    evaMatrix("white")
    light("#ffffff", "off")
    time.sleep(1)
    terminal.insert(INSERT, "\nstate: Entering in stand by mode...")
    while(True): # animacao da luz da matrix
        evaMatrix("white")
        time.sleep(0.5)
        evaMatrix("grey")
        time.sleep(0.5)

# Eva powerOn function
def powerOn():
    x = threading.Thread(target=evaInit, args=())
    x.start()

# set the Eva emotion
def evaEmotion(expression):
    if expression == "neutral":
        canvas.create_image(156, 161, image = im_eyes_neutral)
    elif expression == "angry":
        canvas.create_image(156, 161, image = im_eyes_angry)
    elif expression == "happy":
        canvas.create_image(156, 161, image = im_eyes_happy)
    elif expression == "sad":
        canvas.create_image(156, 161, image = im_eyes_sad)
    elif expression == "power_on": 
        canvas.create_image(156, 161, image = im_eyes_on)
    else: 
        print("Wrong expression")

# set the Eva emotion
def evaMatrix(color):
    if color == "blue":
        canvas.create_image(155, 349, image = im_matrix_blue)
    elif color == "red":
        canvas.create_image(155, 349, image = im_matrix_red)
    elif color == "yellow":
        canvas.create_image(155, 349, image = im_matrix_yellow)
    elif color == "green":
        canvas.create_image(155, 349, image = im_matrix_green)
    elif color == "white":
        canvas.create_image(155, 349, image = im_matrix_white)
    elif color == "grey":
        canvas.create_image(155, 349, image = im_matrix_grey)
    else : 
        print("wrong color to matrix...")

# light color and state
def light(color, state):
    if state == "on":
        canvas.create_oval(300, 205, 378, 285, fill = color, outline = color )
        canvas.create_image(340, 280, image = bulb_image) # redesenha a lampada
    else:
        canvas.create_oval(300, 205, 378, 285, fill = "#000000", outline = "#000000" ) # cor preta indica light off
        canvas.create_image(340, 280, image = bulb_image) # redesenha a lampada

    
# Eva Import Script function
def importFile():
    print("Importing a file...")
    filetypes = (('evaML files', '*.xml'), )
    script_file = fd.askopenfile(mode = "r", title = 'Open an EvaML Script File', initialdir = './', filetypes = filetypes)
    b_run['state'] = NORMAL
    b_stop['state'] = DISABLED
    #evaTalk("Hi Marcio, how are you")
    #terminal.insert(INSERT, "The file " + script_file.name. + " was imported...")

b_power = Button ( window, text = "Power On", command = powerOn)
b_import = Button ( window, text = "Import Script File...", state = DISABLED, command = importFile)
b_run = Button ( window, text = "Run", image = im_bt_play, state = DISABLED, compound=LEFT)
b_stop = Button ( window, text = "Stop", image = im_bt_stop, state = DISABLED, compound=LEFT)

# intro terminal text
terminal.insert(INSERT, " ========================================================== \n")
terminal.insert(INSERT, "       Eva Simulator for EvaML (A XML Based Language)\n               Version 1.0 - UFF/MidiaCom Lab\n")
terminal.insert(INSERT, " ========================================================== ")

#label.pack()
#l_eva.place(x = 0, y = 50)

#l_angry_eyes.place(x = 70, y = 130)
terminal.place(x = 400, y = 60)

b_power.place(x = 400, y = 20)
b_import.place(x = 496, y = 20)
b_run.place(x = 652, y = 20)
b_stop.place(x = 742, y = 20)
    

window.mainloop()