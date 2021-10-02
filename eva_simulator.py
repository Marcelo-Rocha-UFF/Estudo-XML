from tkinter import *
from tkinter import filedialog as fd
from playsound import playsound
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
window.title("Eva Simulator for EvaML (A XML Language Based) - Version 1.0 - UFF/MidiaCom Lab")
window.geometry("838x525")


terminal = Text ( window, fg="black", bg="white", height="32", width="60")

Font_tuple = ("DejaVu Sans Mono", 9)
terminal.configure(font = Font_tuple)



# In order to display the image in a GUI, you will use the 'PhotoImage' method of Tkinter. It will an image from the directory (specified path) and store the image in a variable.
eva_image = PhotoImage(file = "eva.png")
angry_image = PhotoImage(file = "angry_eyes.png")
bulb_image = PhotoImage(file = "bulb.png")

# Finally, to display the image you will make use of the 'Label' method and pass the 'image' variriable as a parameter and use the pack() method to display inside the GUI.
l_eva = Label(window, image = eva_image)
l_bulb = Label(window, image = bulb_image)
l_angry_eyes = Label(window, image = angry_image)

# Eva powerOn function
def powerOn():
    print("Ola")
    l_angry_eyes.place(x = 70, y = 128)
    playsound("my_sounds/power_up.wav", block = True)
    playsound("my_sounds/greetings.mp3", block = False)


# Eva Import Script function
def importFile():
    print("Importing file...")
    filetypes = (
    ('evaML files', '*.xml'), )
    script_file = fd.askopenfile(mode="r", title='Open a EvaML Script File', initialdir='./', filetypes=filetypes)
    #evaTalk("Importing a script file")

b_power = Button ( window, text = "Power On", command = powerOn)
b_import = Button ( window, text = "Import Script File...", command = importFile)

terminal.insert(INSERT, "Eva Simulator for EvaML (A XML Language Based)\nVersion 1.0 - UFF/MidiaCom Lab\n")
terminal.insert(INSERT, "===============================================\n\n")
terminal.insert(INSERT, "Turn on the Robot, import a Script file and have fun!")
#label.pack()
l_eva.place(x = 0, y = 50)
l_bulb.place(x = 290, y = 200)

terminal.place(x = 400, y = 60)
b_power.place(x = 470, y = 20)
b_import.place(x = 580, y = 20)



window.mainloop()