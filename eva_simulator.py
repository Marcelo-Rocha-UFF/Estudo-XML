import hashlib
import os

import random as rnd
import sys
import tkinter
import xml.etree.ElementTree as ET
import eva_memory

from tkinter import *
from tkinter import filedialog as fd
from playsound import playsound
import time
import threading
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# variaveis globais da vm
root = {}
script_node = {}
links_node = {}
fila_links =  [] # fila de links (comandos)

# watson config
apikey = "0UyIQDYcNO7SytoTLOE-hMRME8o7jeAxcD21Bcd7ZZ9E"
url = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/5bd04cd8-cf86-4fbc-b76d-66ee10427604"

# setup watson service
authenticator = IAMAuthenticator(apikey)
# tts service
tts = TextToSpeechV1(authenticator = authenticator)
tts.set_service_url(url)


# Create the Tkinter window
window = Tk()
window.title("Eva Simulator for EvaML - Version 1.0 - UFF/MidiaCom Lab")
window.geometry("838x525")
canvas = Canvas(window, bg = "#d9d9d9", width = 838, height = 525) # o canvas e' necessario para usar imagens com transparencia
canvas.pack()

# Terminal text configuration
terminal = Text ( window, fg = "cyan", bg = "black", height = "32", width = "60")
Font_tuple = ("DejaVu Sans Mono", 9)
terminal.configure(font = Font_tuple)


# Defining the image files
eva_image = PhotoImage(file = "images/eva.png") 
bulb_image = PhotoImage(file = "images/bulb.png")

# eva expressions images
im_eyes_neutral = PhotoImage(file = "images/eyes_neutral.png")
im_eyes_angry = PhotoImage(file = "images/eyes_angry.png")
im_eyes_sad = PhotoImage(file = "images/eyes_sad.png")
im_eyes_happy = PhotoImage(file = "images/eyes_happy.png")
im_eyes_on = PhotoImage(file = "images/eyes_on.png")

# matrix voice images
im_matrix_blue = PhotoImage(file = "images/matrix_blue.png")
im_matrix_green = PhotoImage(file = "images/matrix_green.png")
im_matrix_yellow = PhotoImage(file = "images/matrix_yellow.png")
im_matrix_white = PhotoImage(file = "images/matrix_white.png")
im_matrix_red = PhotoImage(file = "images/matrix_red.png")
im_matrix_grey = PhotoImage(file = "images/matrix_grey.png")

im_bt_play = PhotoImage(file = "images/bt_play.png")
im_bt_stop = PhotoImage(file = "images/bt_stop.png")

# Finally, to display the image you will make use of the 'Label' method and pass the 'image' variriable as a parameter and use the pack() method to display inside the GUI.
#l_eva = Label(canva, image = eva_image)
#l_bulb = Label(canva, image = bulb_image)
#l_angry_eyes = Label(canva, image = angry_image)
canvas.create_image(160, 262, image = eva_image)
canvas.create_oval(300, 205, 377, 285, fill = "#000000", outline = "#000000" ) # cor preta indica light off
canvas.create_image(340, 285, image = bulb_image)


# Eva initialization function
def evaInit():
    bt_power['state'] = DISABLED
    bt_import['state'] = NORMAL
    evaEmotion("power_on")
    playsound("my_sounds/power_on.mp3", block = True)
    terminal.insert(INSERT, "\nstate: Initializing.")
    time.sleep(1)
    evaMatrix("blue")
    # terminal.insert(INSERT, "\nstate: Speaking a greeting text.")
    # playsound("my_sounds/greetings.mp3", block = True)
    # terminal.insert(INSERT, "\nstate: Turning on the blue light.")
    # light("blue", "on")
    # time.sleep(2)
    # terminal.insert(INSERT, "\nstate: Turning on the red light.")
    # light("red", "on")
    # time.sleep(2)
    # terminal.insert(INSERT, "\nstate: Turning on the green light.")
    # light("green", "on")
    # time.sleep(2)
    # terminal.insert(INSERT, "\nstate: Turning on the white light.")
    # light("white", "on")
    # time.sleep(2)
    # evaEmotion("angry")
    # light("white", "on")
    # evaMatrix("red")
    # terminal.insert(INSERT, "\nstate: Expressing anger.")
    # time.sleep(2)
    # evaEmotion("happy")
    # evaMatrix("yellow")
    # terminal.insert(INSERT, "\nstate: Expressing joy.")
    # time.sleep(2)
    # evaEmotion("sad")
    # evaMatrix("blue")
    # terminal.insert(INSERT, "\nstate: Expressing sadness.")
    # time.sleep(2)
    # evaEmotion("neutral")
    # terminal.insert(INSERT, "\nstate: Turning off the light.")
    # light("#ffffff", "off")
    # time.sleep(2)
    terminal.insert(INSERT, '\nstate: Speaking: "Load a script file and enjoy."')
    playsound("my_sounds/load_a_script.mp3", block = True)
    terminal.insert(INSERT, "\nstate: Entering in standby mode.")
    # while(True): # animacao da luz da matrix
    #     evaMatrix("white")
    #     time.sleep(0.5)
    #     evaMatrix("grey")
    #     time.sleep(0.5)


# Eva powerOn function
def powerOn():
    threading.Thread(target=evaInit, args=()).start()

def runScript():
    busca_links("1000")
    threading.Thread(target=link_process, args=()).start()
    

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
    time.sleep(1)

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
    color_map = {"white":"#ffffff", "black":"#000000", "red":"#ff0000", "pink":"#e6007e", "green":"#00ff00", "yellow":"#ffff00", "blue":"#0000ff"}
    if color_map.get(color) != None:
        color = color_map.get(color)
    if state == "on":
        canvas.create_oval(300, 205, 377, 285, fill = color, outline = color )
        canvas.create_image(340, 285, image = bulb_image) # redesenha a lampada
    else:
        canvas.create_oval(300, 205, 377, 285, fill = "#000000", outline = "#000000" ) # cor preta indica light off
        canvas.create_image(340, 285, image = bulb_image) # redesenha a lampada

    
# Eva Import Script function
def importFile():
    global root, script_node, links_node
    print("Importing a file...")
    filetypes = (('evaML files', '*.xml'), )
    script_file = fd.askopenfile(mode = "r", title = 'Open an EvaML Script File', initialdir = './', filetypes = filetypes)
    # variaveis da vm
    tree = ET.parse(script_file)  # arquivo de codigo xml
    root = tree.getroot() # evaml root node
    script_node = root.find("script")
    links_node = root.find("links")
    bt_run['state'] = NORMAL
    bt_stop['state'] = DISABLED
    #evaTalk("Hi Philip, let's go to play guitar")
    #terminal.insert(INSERT, "The file " + script_file.name. + " was imported...")

bt_power = Button ( window, text = "Power On", command = powerOn)
bt_import = Button ( window, text = "Import Script File...", state = DISABLED, command = importFile)
bt_run = Button ( window, text = "Run", image = im_bt_play, state = DISABLED, compound = LEFT, command = runScript)
bt_stop = Button ( window, text = "Stop", image = im_bt_stop, state = DISABLED, compound = LEFT)

# intro terminal text
terminal.insert(INSERT, "============================================================\n")
terminal.insert(INSERT, "                  Eva Simulator for EvaML\n               Version 1.0 - UFF/MidiaCom Lab\n")
terminal.insert(INSERT, "============================================================")

#label.pack()
#l_eva.place(x = 0, y = 50)

#l_angry_eyes.place(x = 70, y = 130)
terminal.place(x = 400, y = 60)

bt_power.place(x = 400, y = 20)
bt_import.place(x = 496, y = 20)
bt_run.place(x = 652, y = 20)
bt_stop.place(x = 742, y = 20)

# funcoes da vm
# executa os comandos
def exec_comando(node):
    if node.tag == "voice":
        terminal.insert(INSERT, "\nstate: Selected Voice: " + node.attrib["tone"])
        terminal.see(tkinter.END)

    elif node.tag == "light":
        state = node.attrib["state"]
        color = node.attrib["color"]
        if state == "on":
            terminal.insert(INSERT, "\nstate: Turnning on the light. Color = " + color + ".")
            terminal.see(tkinter.END) # autoscrolling
        else:
            terminal.insert(INSERT, "\nstate: Turnning off the light.")
            terminal.see(tkinter.END)
        light(color , state)
        time.sleep(1) # emula o tempo da lampada real

    elif node.tag == "wait":
        duration = node.attrib["duration"]
        terminal.insert(INSERT, "\nstate: Pausing. Duration = " + duration + " ms")
        terminal.see(tkinter.END)
        time.sleep(int(duration)/1000) # converte para segundos

    elif node.tag == "random":
        min = node.attrib["min"]
        max = node.attrib["max"]
        eva_memory.var_dolar.append(str(rnd.randint(int(min), int(max))))
        terminal.insert(INSERT, "\nstate: Generating a random number: " + eva_memory.var_dolar[-1])
        terminal.see(tkinter.END)
        print("random command, min = " + min + ", max = " + max + ", valor = " + eva_memory.var_dolar[-1])

    elif node.tag == "listen":
        print("listen command")

    elif node.tag == "talk":
        texto = node.text
        # esta parte substitui o $ no texto
        if len(eva_memory.var_dolar) != 0:
            texto = texto.replace("$", eva_memory.var_dolar[-1])

        # esta parte implementa o texto aleatorio gerado pelo uso do caractere /
        texto = texto.split(sep="/") # texto vira um lista com a qtd de frases divididas pelo caract. /
        ind_random = rnd.randint(0, len(texto)-1)
        print("ind_random", ind_random, texto[ind_random])
        terminal.insert(INSERT, '\nstate: Speaking: "' + texto[ind_random] + '"')
        terminal.see(tkinter.END)

        # Assume the default UTF-8 (Gera o hashing do arquivo de audio)
        hash_object = hashlib.md5(texto[ind_random].encode())
        file_name = "_audio_" + hash_object.hexdigest()

        # verifica se o audio da fala já existe na pasta
        if not (os.path.isfile("audio_cache_files/" + file_name + ".mp3")): # se nao existe chama o watson
            # Eva tts functions
            with open("audio_cache_files/" + file_name + ".mp3", 'wb') as audio_file:
                res = tts.synthesize(texto[ind_random], accept = "audio/mp3", voice = root.find("settings")[0].attrib["tone"]).get_result()
                audio_file.write(res.content)
        evaMatrix("blue")
        playsound("audio_cache_files/" + file_name + ".mp3", block = True) # toca o audio da fala
        evaMatrix("white")

    elif node.tag == "evaEmotion":
        emotion = node.attrib["emotion"]
        terminal.insert(INSERT, "\nstate: Expressing an emotion: " + emotion)
        terminal.see(tkinter.END)
        if emotion == "angry":
            evaMatrix("red")
        elif emotion == "happy":
            evaMatrix("yellow")
        elif emotion == "sad":
            evaMatrix("blue")
        elif emotion == "neutral":
            evaMatrix("white")
        evaEmotion(emotion)

    elif node.tag == "audio":
        audio_file = "sonidos/" + node.attrib["source"] + ".wav"
        block = False # o play do audio não bloqueia a execucao do script
        if node.attrib["block"].lower() == "true":
            block = True
        terminal.insert(INSERT, '\nstate: Playing a sound: "' + node.attrib["source"] + ".wav" + '", block=' + str(block))
        terminal.see(tkinter.END)
        playsound(audio_file, block = block)

    elif node.tag == "case":
        eva_memory.reg_case = 0 # limpa o flag do case
        valor = node.attrib["value"]
        print("valor ", valor, type(valor))
        if valor == eva_memory.var_dolar[-1]: # compara valor com o topo da pilha da variavel var_dolar
            eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

    elif node.tag == "counter":
        var_name = node.attrib["var"]
        var_value = int(node.attrib["value"])
        op = node.attrib["op"]
        if op == "=": # efetua a atribuicao
            eva_memory.vars[var_name] = var_value

        if op == "+": # efetua a adição
            eva_memory.vars[var_name] += var_value

        if op == "*": # efetua o produto
            eva_memory.vars[var_name] *= var_value

        if op == "/": # efetua a divisão
            eva_memory.vars[var_name] /= var_value

        if op == "%": # calcula o módulo
            eva_memory.vars[var_name] %= var_value
        
        print("Eva ram => ", eva_memory.vars)
        terminal.insert(INSERT, "\nstate: Counter : var=" + var_name + ", value=" + str(var_value) + ", op(" + op + "), result=" + str(eva_memory.vars[var_name]))
        terminal.see(tkinter.END)

def busca_commando(key): # keys são strings
	# busca em settings. Isto porque "voice" fica em settings
	for elem in root.find("settings").iter():
		if elem.get("key") != None: # verifica se node tem atributo id
			if elem.attrib["key"] == key:
				return elem
	# busca dentro do script
	for elem in root.find("script").iter(): # passa por todos os nodes do script
		if elem.get("key") != None: # verifica se node tem atributo id
			if elem.attrib["key"] == key:
				return elem


# busca e insere na lista os links que tem att_from igual ao from do link
def busca_links(att_from):
    achou_link = False
    for i in range(len(links_node)):
        if att_from == links_node[i].attrib["from"]:
            fila_links.append(links_node[i])
            achou_link = True
    return achou_link


# executa os comandos que estão na pilha de links
def link_process(anterior = -1):
    terminal.insert(INSERT, "\n---------------------------------------------------")
    terminal.insert(INSERT, "\nstate: Starting the script: " + root.attrib["name"])
    terminal.see(tkinter.END)
    global fila_links
    while len(fila_links) != 0:
        from_key = fila_links[0].attrib["from"] # chave do comando a executar
        to_key = fila_links[0].attrib["to"] # chave do próximo comando
        comando_from = busca_commando(from_key).tag # Tag do comando a ser executado
        comando_to = busca_commando(to_key).tag # DEBUG

        # evita que um mesmo nó seja executado consecutivamente
        if anterior != from_key:
            exec_comando(busca_commando(from_key))
            anterior = from_key
        
        if comando_from == "case": # se o comando executado foi um case
            if eva_memory.reg_case == 1: # verifica a flag pra saber se o case foi verdadeiro
                fila_links = [] # esvazia a fila, pois o fluxo seguira deste no case em diante
                print("case command")
                # segue o fluxo do case de sucesso buscando o prox. link
                if not(busca_links(to_key)): # se nao tem mais link, o comando indicado por to_key é o ultimo do fluxo
                    exec_comando(busca_commando(to_key))
                    print("fim de bloco.............")
            else:
                fila_links.pop(0) # se o case falhou, ele é retirado da fila e consequentemente seu fluxo é descartado
                print("false")
        else: # se o comando nao foi um case
            fila_links.pop(0) # remove o link da fila
            if not(busca_links(to_key)): # como já comentado anteriormente
                exec_comando(busca_commando(to_key))
                print("fim de bloco.............")
    terminal.insert(INSERT, "\nstate: End of script.")
    terminal.see(tkinter.END)

window.mainloop()