#!/usr/bin/env python
import hashlib
from logging import _levelToName
import os

import random as rnd
import sys
import xml.etree.ElementTree as ET

from ibm_watson.text_to_speech_v1 import Voice
import eva_memory # modulo de memoria do EvaSIM

from tkinter import *
from tkinter import filedialog as fd
import tkinter

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
thread_pop_pause = False


# funcao de controle da variavel que bloqueia as janelas popups
def lock_thread_pop():
    global thread_pop_pause
    thread_pop_pause = True

def unlock_thread_pop():
    global thread_pop_pause
    thread_pop_pause = False


# watson config api key
with open("ibm_cred.txt", "r") as ibm_cred:
    ibm_config = ibm_cred.read().splitlines()
apikey = ibm_config[0]
url = ibm_config[1]
# setup watson service
authenticator = IAMAuthenticator(apikey)
# tts service
tts = TextToSpeechV1(authenticator = authenticator)
tts.set_service_url(url)


# Create the Tkinter window
window = Tk()
window.title("Eva Simulator for EvaML - Version 1.0 - UFF/MidiaCom/CICESE")
w = 945
h = 525
window.geometry(str(w) + "x" + str(h))
canvas = Canvas(window, bg = "#d9d9d9", width = w, height = h) # o canvas e' necessario para usar imagens com transparencia
canvas.pack()
# Terminal text configuration
terminal = Text ( window, fg = "cyan", bg = "black", height = "32", width = "75")
terminal.configure(font = ("DejaVu Sans Mono", 9))
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
# desenha o eva e a lampada desligada
canvas.create_image(160, 262, image = eva_image)
canvas.create_oval(300, 205, 377, 285, fill = "#000000", outline = "#000000" ) # cor preta indica light off
canvas.create_image(340, 285, image = bulb_image)


# Eva initialization function
def evaInit():
    bt_power['state'] = DISABLED
    evaEmotion("power_on")
    terminal.insert(INSERT, "\nstate: Initializing.")
    playsound("my_sounds/power_on.mp3", block = True)
    terminal.insert(INSERT, "\nstate: Speaking a greeting text.")
    playsound("my_sounds/greetings.mp3", block = True)
    terminal.insert(INSERT, '\nstate: Speaking "Load a script file and enjoy."')
    playsound("my_sounds/load_a_script.mp3", block = True)
    terminal.insert(INSERT, "\nstate: Entering in standby mode.")
    bt_import['state'] = NORMAL
    while bt_run['state'] == DISABLED: # animacao da luz da matrix em stand by
            evaMatrix("white")
            time.sleep(0.5)
            evaMatrix("grey")
            time.sleep(0.5)


# Eva powerOn function
def powerOn():
    threading.Thread(target=evaInit, args=()).start()


# Ativa a thread que roda o script
def runScript():
    busca_links("1000")
    threading.Thread(target=link_process, args=()).start()


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
    evaEmotion("neutral")
    terminal.insert(INSERT, '\nstate: Script loaded.')
    terminal.see(tkinter.END)

def clear_terminal():
    terminal.delete('1.0', END)
    # criando terminal text
    terminal.insert(INSERT, "===========================================================================\n")
    terminal.insert(INSERT, "                         Eva Simulator for EvaML\n                Version 1.0 - UFF/MidiaCom/CICESE [2021]\n")
    terminal.insert(INSERT, "===========================================================================")

# criacao dos botoes da interface com usuário
bt_power = Button ( window, text = "Power On", command = powerOn)
bt_import = Button ( window, text = "Import Script File...", state = DISABLED, command = importFile)
bt_run = Button ( window, text = "Run", image = im_bt_play, state = DISABLED, compound = LEFT, command = runScript)
bt_stop = Button ( window, text = "Stop", image = im_bt_stop, state = DISABLED, compound = LEFT)
bt_clear = Button ( window, text = "Clear Term.", state = NORMAL, compound = LEFT, command = clear_terminal)
# limpa e desenha o texto padrao do terminal
clear_terminal()
terminal.place(x = 400, y = 60)
bt_power.place(x = 400, y = 20)
bt_import.place(x = 496, y = 20)
bt_run.place(x = 652, y = 20)
bt_stop.place(x = 742, y = 20)
bt_clear.place(x = 835, y = 20)


# led "animations"
def ledAnimation(animation):
    if animation == "stop": evaMatrix("grey")
    elif animation == "listen": evaMatrix("green")
    elif animation == "speak": evaMatrix("blue")
    elif animation == "angry": evaMatrix("red")
    elif animation == "happy": evaMatrix("green")
    elif animation == "sad": evaMatrix("blue")
    elif animation == "surprise": evaMatrix("yellow")
    else: print("wrong led animation option")


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


# set the Eva matrix
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


# set the iamge of light (color and state)
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


# funcoes da maquina virtual
# executa os comandos
def exec_comando(node):
    if node.tag == "voice":
        terminal.insert(INSERT, "\nstate: Selected Voice: " + node.attrib["tone"])
        terminal.see(tkinter.END)


    elif node.tag == "light":
        state = node.attrib["state"]
        # caso a seguir, se o sate é off, e pode não ter atributo color definido
        if state == "off":
            color = "black"
            terminal.insert(INSERT, "\nstate: Turnning off the light.")
            terminal.see(tkinter.END)
        else:
            color = node.attrib["color"]
            terminal.insert(INSERT, "\nstate: Turnning on the light. Color=" + color + ".")
            terminal.see(tkinter.END) # autoscrolling
        light(color , state)
        time.sleep(1) # emula o tempo da lampada real


    elif node.tag == "wait":
        duration = node.attrib["duration"]
        terminal.insert(INSERT, "\nstate: Pausing. Duration=" + duration + " ms")
        terminal.see(tkinter.END)
        time.sleep(int(duration)/1000) # converte para segundos


    elif node.tag == "led":
        ledAnimation(node.attrib["animation"])
        terminal.insert(INSERT, "\nstate: Matrix Leds. Animation=" + node.attrib["animation"])
        terminal.see(tkinter.END)


    elif node.tag == "random":
        min = node.attrib["min"]
        max = node.attrib["max"]
        eva_memory.var_dolar.append(str(rnd.randint(int(min), int(max))))
        terminal.insert(INSERT, "\nstate: Generating a random number: " + eva_memory.var_dolar[-1])
        terminal.see(tkinter.END)
        print("random command, min = " + min + ", max = " + max + ", valor = " + eva_memory.var_dolar[-1])


    elif node.tag == "listen":
        lock_thread_pop()
        ledAnimation("listen")
        # função de fechamento da janela pop up
        def fechar_pop(): 
            print(var.get())
            eva_memory.var_dolar.append(var.get())
            terminal.insert(INSERT, "\nstate: Listening : var=$" + ", value=" + eva_memory.var_dolar[-1])
            terminal.see(tkinter.END)
            pop.destroy()
            unlock_thread_pop() # reativa a thread de processamento do script
        # criacao da janela
        var = StringVar()
        pop = Toplevel(window)
        pop.title("Listen Command")
        w = 300
        h = 150
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)  
        pop.geometry('%dx%d+%d+%d' % (w, h, x, y))
        pop.grab_set()
        label = Label(pop, text="Eva is listening... Please, enter your answer!", font = ('Aerial', 9))
        label.pack(pady=20)
        Entry(pop, textvariable = var, font = ('Aerial', 9)).pack()
        # E1.bind("<Return>", fechar_pop)
        # E1.pack()
        Button(pop, text="    OK    ", command=fechar_pop).pack(pady=20)
        # espera pela liberacao, aguardando a resposta do usuario
        while thread_pop_pause: 
            time.sleep(0.5)
        ledAnimation("stop")


    elif node.tag == "talk":
        texto = node.text
        # substitui as variaveis pelo texto. as variaveis devem existir na memoria
        texto_aux = texto
        for i in range(len(texto)):
            if texto[i] == "#":
                inicio = i
                while texto[i] != " ":
                    i += 1
                    if i == len(texto):
                        break
                if i - inicio > 0:
                    for v in eva_memory.vars:
                        if v == texto[inicio + 1: i]:
                            texto_aux = texto_aux.replace(texto[inicio: i], str(eva_memory.vars[v]))
        texto = texto_aux

        # esta parte substitui o $, ou o $-1 ou o $1 no texto
        if "$" in texto: # verifica se tem $ no texto
            if len(eva_memory.var_dolar) != 0: # verifica se tem conteudo em $
                # Obs, a ordem importa na comparacao a seguir
                if "$-1" in texto:
                    texto = texto.replace("$-1", eva_memory.var_dolar[-2])
                if "$1" in texto:
                    texto = texto.replace("$1", eva_memory.var_dolar[0])
                if "$" in texto:
                    texto = texto.replace("$", eva_memory.var_dolar[-1])
            else:
                print("Erro: A variável $ não possui qualquer valor e não pode ser utilizada.")
                exit(1)
        # esta parte implementa o texto aleatorio gerado pelo uso do caractere /
        texto = texto.split(sep="/") # texto vira uma lista com a qtd de frases divididas pelo caract. /
        ind_random = rnd.randint(0, len(texto)-1)
        terminal.insert(INSERT, '\nstate: Speaking: "' + texto[ind_random] + '"')
        terminal.see(tkinter.END)

        # Assume the default UTF-8 (Gera o hashing do arquivo de audio)
        hash_object = hashlib.md5(texto[ind_random].encode())
        file_name = "_audio_"  + root.find("settings")[0].attrib["tone"] + hash_object.hexdigest()

        # verifica se o audio da fala já existe na pasta
        if not (os.path.isfile("audio_cache_files/" + file_name + ".mp3")): # se nao existe chama o watson
            # Eva tts functions
            with open("audio_cache_files/" + file_name + ".mp3", 'wb') as audio_file:
                res = tts.synthesize(texto[ind_random], accept = "audio/mp3", voice = root.find("settings")[0].attrib["tone"]).get_result()
                audio_file.write(res.content)
        ledAnimation("speak")
        playsound("audio_cache_files/" + file_name + ".mp3", block = True) # toca o audio da fala
        ledAnimation("stop")


    elif node.tag == "evaEmotion":
        emotion = node.attrib["emotion"]
        terminal.insert(INSERT, "\nstate: Expressing an emotion: " + emotion)
        terminal.see(tkinter.END)
        evaEmotion(emotion)


    elif node.tag == "audio":
        audio_file = "sonidos/" + node.attrib["source"] + ".wav"
        block = False # o play do audio não bloqueia a execucao do script
        if node.attrib["block"].lower() == "true":
            block = True
        terminal.insert(INSERT, '\nstate: Playing a sound: "' + node.attrib["source"] + ".wav" + '", block=' + str(block))
        terminal.see(tkinter.END)
        ledAnimation("speak")
        playsound(audio_file, block = block)
        ledAnimation("stop")


    elif node.tag == "case": 
        global valor
        eva_memory.reg_case = 0 # limpa o flag do case
        valor = node.attrib["value"]
        valor = valor.lower() # as comparacoes não são case sensitive
        # trata os tipos de comparacao e operadores
        # caso 1. Var=$.
        if node.attrib['var'] == "$":
            # case 1.1 (tipo de op="exact")
            if node.attrib['op'] == "exact":
                if "#" in valor: # verifica se valor é uma variável
                    print("valor ", valor, type(valor))
                    if eva_memory.var_dolar[-1] == str(eva_memory.vars[valor[1:]]).lower(): # compara valor $ com a variavel #..
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
                else:    
                    print("valor ", valor, type(valor))
                    if valor == eva_memory.var_dolar[-1].lower(): # compara valor com o topo da pilha da variavel var_dolar
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

            # case 1.2 (tipo de op="contain")
            elif node.attrib['op'] == "contain":
                if "#" in valor: # verifica se valor é uma variável
                    print("valor ", valor, type(valor))
                    if str(eva_memory.vars[valor[1:]]).lower() in eva_memory.var_dolar[-1]: # verifica se var #.. está contida em $
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
                else:    
                    print("valor ", valor, type(valor))
                    if valor in eva_memory.var_dolar[-1].lower(): # verifica se valor está contido em $
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira


### PRECISA DE TESTE         
            # case 1.3 (tipo de op="MATEMATICA") Comparando $ com uma var (em valor) de maneira matemática
            if "#" in valor: # verifica se valor é uma variável
                if node.attrib['op'] == "eq": # 
                    if int(eva_memory.var_dolar[-1]) == int(eva_memory.vars[valor[1:]]): # é preciso retirar o # da variável
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                elif node.attrib['op'] == "lt": # igualdade
                    if int(eva_memory.var_dolar[-1]) < int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                elif node.attrib['op'] == "gt": # igualdade
                    if int(eva_memory.var_dolar[-1]) > int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
                
                elif node.attrib['op'] == "lte": # igualdade
                    if int(eva_memory.var_dolar[-1]) <= int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                elif node.attrib['op'] == "gte": # igualdade
                    if int(eva_memory.var_dolar[-1]) >= int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                elif node.attrib['op'] == "ne": # igualdade
                    if int(eva_memory.var_dolar[-1]) != int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
            

            else: # case 1.4 comparação MATEMÁTICA entre $ e uma constante
                if node.attrib['op'] == "eq": # 
                    if int(eva_memory.var_dolar[-1]) == int(valor): # converte valor para int (comparação matemática)
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                elif node.attrib['op'] == "lt": # igualdade
                    if int(eva_memory.var_dolar[-1]) < int(valor):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                elif node.attrib['op'] == "gt": # igualdade
                    if int(eva_memory.var_dolar[-1]) > int(valor):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
                
                elif node.attrib['op'] == "lte": # igualdade
                    if int(eva_memory.var_dolar[-1]) <= int(valor):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                elif node.attrib['op'] == "gte": # igualdade
                    if int(eva_memory.var_dolar[-1]) >= int(valor):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                elif node.attrib['op'] == "ne": # igualdade
                    if int(eva_memory.var_dolar[-1]) != int(valor):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
########
   
        else: # caso var seja uma variável, tipo #x. É UMA COMPARAÇÃO MATEMÁTICA, USA NÚMEROS
            # case 2.1 - comparando var com outra var
            if "#" in valor: # valor é uma variável
                if node.attrib['op'] == "eq": # testa a igualdade do valor contido em var com o valor da var contida "valor".
                    if int(eva_memory.vars[node.attrib['var']]) == int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "lt": # menor que
                    if int(eva_memory.vars[node.attrib['var']]) < int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "gt": # maior que
                    if int(eva_memory.vars[node.attrib['var']]) > int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
                
                if node.attrib['op'] == "lte": # menor ou igual
                    if int(eva_memory.vars[node.attrib['var']]) <= int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "gte": # maior ou igual
                    if int(eva_memory.vars[node.attrib['var']]) >= int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "ne": # diferente
                    if int(eva_memory.vars[node.attrib['var']]) != int(eva_memory.vars[valor[1:]]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira


            # case 2.2 - comparando var com $
            elif "$" in valor: # valor é $
                if node.attrib['op'] == "eq": # testa a igualdade do valor contido em var com o $".
                    if int(eva_memory.vars[node.attrib['var']]) == int(eva_memory.var_dolar[-1]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "lt": # menor que
                    if int(eva_memory.vars[node.attrib['var']]) < int(eva_memory.var_dolar[-1]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "gt": # maior que
                    if int(eva_memory.vars[node.attrib['var']]) > int(eva_memory.var_dolar[-1]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
                
                if node.attrib['op'] == "lte": # menor ou igual
                    if int(eva_memory.vars[node.attrib['var']]) <= int(eva_memory.var_dolar[-1]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "gte": # maior ou igual
                    if int(eva_memory.vars[node.attrib['var']]) >= int(eva_memory.var_dolar[-1]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "ne": # diferente
                    if int(eva_memory.vars[node.attrib['var']]) != int(eva_memory.var_dolar[-1]):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira


            # case 2.3 - comparando var com um valor constante
            else: # valor é uma variável
                if node.attrib['op'] == "eq": # testa a igualdade do valor contido em var com uma constante dentro de valor.
                    if int(eva_memory.vars[node.attrib['var']]) == int(node.attrib['value']):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "lt": # menor que
                    if int(eva_memory.vars[node.attrib['var']]) < int(node.attrib['value']):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "gt": # maior que
                    if int(eva_memory.vars[node.attrib['var']]) > int(node.attrib['value']):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
                
                if node.attrib['op'] == "lte": # menor ou igual
                    if int(eva_memory.vars[node.attrib['var']]) <= int(node.attrib['value']):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "gte": # maior ou igual
                    if int(eva_memory.vars[node.attrib['var']]) >= int(node.attrib['value']):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira

                if node.attrib['op'] == "ne": # diferente
                    if int(eva_memory.vars[node.attrib['var']]) != int(node.attrib['value']):
                        eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira
                


    elif node.tag == "default": # default sempre será verdadeiro
        print("Default funcionando")
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


    elif node.tag == "userEmotion":
        global img_neutral, img_happy, img_angry, img_sad, img_surprised
        lock_thread_pop()

        def fechar_pop(): # função de fechamento da janela pop up
            print(var.get())
            eva_memory.var_dolar.append(var.get())
            terminal.insert(INSERT, "\nstate: userEmotion : var=$" + ", value=" + eva_memory.var_dolar[-1])
            terminal.see(tkinter.END)
            pop.destroy()
            unlock_thread_pop() # reativa a thread de processamento do script

        var = StringVar()
        var.set("Neutral")
        img_neutral = PhotoImage(file = "images/img_neutral.png")
        img_happy = PhotoImage(file = "images/img_happy.png")
        img_angry = PhotoImage(file = "images/img_angry.png")
        img_sad = PhotoImage(file = "images/img_sad.png")
        img_surprised = PhotoImage(file = "images/img_surprised.png")
        pop = Toplevel(window)
        pop.title("userEmotion Command")
        w = 697
        h = 250
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)  
        pop.geometry('%dx%d+%d+%d' % (w, h, x, y))
        pop.grab_set() # faz com que a janela receba todos os eventos
        Label(pop, text="Eva is analysing your face expression. Please, choose one emotion!", font = ('Aerial', 12)).place(x = 95, y = 10)
        # imagens são exibidas usando os lables
        Label(pop, image=img_neutral).place(x = 10, y = 50)
        Label(pop, image=img_happy).place(x = 147, y = 50)
        Label(pop, image=img_angry).place(x = 284, y = 50)
        Label(pop, image=img_sad).place(x = 421, y = 50)
        Label(pop, image=img_surprised).place(x = 558, y = 50)
        Radiobutton(pop, text = "Neutral", variable = var, command = None, value = "neutral").place(x = 35, y = 185)
        Radiobutton(pop, text = "Happy", variable = var, command = None, value = "happy").place(x = 172, y = 185)
        Radiobutton(pop, text = "Angry", variable = var, command = None, value = "angry").place(x = 312, y = 185)
        Radiobutton(pop, text = "Sad", variable = var, command = None, value = "sad").place(x = 452, y = 185)
        Radiobutton(pop, text = "Surprised", variable = var, command = None, value = "surprised").place(x = 575, y = 185)
        Button(pop, text = "     OK     ", command = fechar_pop).place(x = 310, y = 215)
        # espera pela liberacao, aguardando a resposta do usuario
        while thread_pop_pause: 
            time.sleep(0.5)


def busca_commando(key): # keys são strings
	# busca em settings. Isto porque "voice" fica em settings e voice é sempre o primeiro elemento
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

        # evita que um mesmo nó seja executado consecutivamente. Isso acontece com o nó que antecede os cases
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
