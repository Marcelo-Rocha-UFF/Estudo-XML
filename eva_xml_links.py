import sys
import json
import xml.etree.ElementTree as ET
import send_to_dbjson

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
output = ""
gohashid = 0
inicio = True  # para nao iniciar com a virgula
pilha = [] # pilha de nodes (enderecos)

def block_process(root):
    global output, inicio
    for command in root:
        if (command.tag == 'audio'):
            if (not inicio): output += ",\n"
            output += audio_process(command)

        if (command.tag == 'light'):
            if (not inicio): output += ",\n"
            output += light_process(command)

        if (command.tag == 'wait'):
            if (not inicio): output += ",\n"
            output += wait_process(command)

        # the voice nodes are only process in the settings section
        # if (command.tag == 'voice'):
        #     if (not inicio): output += ",\n"
        #     output += voice_process(command)

        if (command.tag == 'talk'):
            if (not inicio): output += ",\n"
            output += talk_process(command)

        if (command.tag == 'random'):
            if (not inicio): output += ",\n"
            output += random_process(command)

        if (command.tag == 'listen'):
            if (not inicio): output += ",\n"
            output += listen_process(command)

        if (command.tag == 'evaEmotion'):
            if (not inicio): output += ",\n"
            output += eva_emotion_process(command)

        if (command.tag == 'case'):
            if (not inicio): output += ",\n"
            output += case_process(command)
            block_process(command)

        # default é um caso especial do comando case, onde value = ""
        if (command.tag == 'default'):
            command.attrib["value"] = ""
            if (not inicio): output += ",\n"
            output += case_process(command)
            block_process(command)

        # switch is just an abstraction not a real node
        if (command.tag == 'switch'):
            block_process(command)

        # macro is just an abstraction
        if (command.tag == 'macro'):
            print("processando macro")
            block_process(command)

        inicio = False

# head processing (generates the head of json file)
def head_process(node):
    node.attrib["key"] = str(0)
    init = """{
  "_id": """ + '"' + node.attrib["id"] + '",' + """
  "nombre": """ + '"' + node.attrib['name'] + '",' + """
  "data": {
    "node": [
"""
    return init

# processing the settings nodes
# always be the first node in the interaccion
def settings_process(node):
    return voice_process(node.find("voice")) + ",\n"
    # processar light-effects
    # processar sound-effects

# audio node processing
def audio_process(audio_command):
    global gohashid
    audio_node = """      {
        "key": """ + audio_command.attrib["key"] + """,
        "name": "Audio",
        "type": "sound",
        "color": "lightblue",
        "isGroup": false,
        "src": """ + '"' + audio_command.attrib['source'] + '",' + """
        "wait": """ + audio_command.attrib['wait'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return audio_node

# light node processing
def light_process(light_command):
    global gohashid
    light_node = """      {
        "key": """ + light_command.attrib["key"] + """,
        "name": "Light",
        "type": "light",
        "color": "lightblue",
        "isGroup": false,
        "group": "",
        "lcolor": """ + '"' + light_command.attrib['color'] + '",' + """
        "state": """ + '"' + light_command.attrib['state'] + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return light_node

# listen node processing
def listen_process(listen_command):
    global gohashid, key
    listen_node = """      {
        "key": """ + listen_command.attrib["key"] + """,
        "name": "Listen",
        "type": "listen",
        "color": "lightblue",
        "isGroup": false,
        "group": "",
        "lcolor": "zzz",
        "state": "zzz",
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return listen_node

# talk node processing
def talk_process(talk_command):
    global gohashid, key
    talk_node = """      {
        "key": """ + talk_command.attrib["key"] + """,
        "name": "Talk",
        "type": "speak",
        "color": "lightblue",
        "isGroup": false,
        "text": """ + '"' + talk_command.text + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return talk_node



# voice node processing
def voice_process(voice_command):
    global gohashid
    voice_node = """      {
        "key": """ + voice_command.attrib["key"] + """,
        "name": "Voice",
        "type": "voice",
        "color": "lightblue",
        "isGroup": false,
        "voice": """ + '"' + voice_command.attrib['tone'] + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return voice_node


# eva_emotion node processing 
def eva_emotion_process(eva_emotion_command):
    global gohashid
    eva_emotion_node = """      {
        "key": """ + eva_emotion_command.attrib["key"] + """,
        "name": "Eva_Emotion",
        "type": "emotion",
        "color": "lightyellow",
        "isGroup": false,
        "group": "",
        "emotion": """ + '"' + eva_emotion_command.attrib['emotion'] + '",' + """
        "level": 0,
        "speed": 0,
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return eva_emotion_node


# random node processing
def random_process(random_command):
    global gohashid
    random_node = """      {
        "key": """ + random_command.attrib["key"] + """,
        "name": "Random",
        "type": "random",
        "color": "lightblue",
        "isGroup": false,
        "group": "",
        "min": """ + random_command.attrib['min'] + ',' + """
        "max": """ + random_command.attrib['max'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return random_node


# condition node (case and default) processing
def case_process(case_command):
    global gohashid
    case_node = """      {
        "key": """ + case_command.attrib["key"] + """,
        "name": "Condition",
        "type": "if",
        "color": "lightblue",
        "isGroup": false,
        "text": """ + '"' + case_command.attrib['value'] + '",' + """
        "opt": 4,
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return case_node

# wait node processing
def wait_process(wait_command):
    global gohashid
    wait_node = """      {
        "key": """ + wait_command.attrib["key"] + """,
        "name": "Wait",
        "type": "wait",
        "color": "lightblue",
        "isGroup": false,
        "time": """ + wait_command.attrib['duration'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return wait_node



###############################################################################
# aqui estão os métodos que geram os links que conectam os nós                #
###############################################################################

links = [] # lista provisoria com os links gerados

def cria_link(node_from, node_to):
    # node stop como node_to
    if (node_to.tag == "stop"): # stop nao pode ser node_to
        return

    # um switch, uma macro, um goto ou um stop nunca podem ser node_from
    if node_from.tag == "switch": return
    if node_from.tag == "macro": return
    if node_from.tag == "stop": return
    if node_from.tag == "goto": return

    # node goto com node_to
    if node_to.tag == "goto":
        for elem in script_node.iter(): # procura por target na interação
            if elem.get("id") != None:
                if elem.attrib["id"] == node_to.attrib["target"]:
                    links.append(node_from.attrib["key"] + "," + elem.attrib["key"])
        return

    # no "to" e' uma folha, que nao contem filhos
    if len(node_to) == 0:
        links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])
        
    # trata os nodes com filhos
    elif (node_to.tag == "switch"): # trata o node "switch"
        for switch_elem in node_to:
            links.append(node_from.attrib["key"] + "," + switch_elem.attrib["key"])
            link_process(switch_elem, switch_elem)
    elif (node_to.tag == "case"): # trata o node "case"
        links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])
        link_process(node_to, node_to)
    elif (node_to.tag == "macro"): # trata de node "macro"
        link_process(node_from, node_to)

def link_process(node_from, node_list):
    qtd = len(node_list)
    node_to = node_list[0]
    cria_link(node_from, node_to)
    for i in range(0, qtd-1):
        node_from = node_list[i]
        node_to = node_list[i+1]
        ########################################
        if node_to.tag == "switch":
            if (i+1 != qtd-1): # verifica se existe algum node, dentro do fluxo corrente, depois do switch
                for p in range(0, len(node_to)): # empilhando no' depois do switch
                    # a qtd de empilhamentos e' igual ao numero de cases dentro do switch
                    pilha.append(node_list[i+2])
            else: # quando não ha no' depois do switch
                if len(pilha) != 0: # um switch com uma pilha nao vazia e' um switch interno a outro switch
                    no_aux = pilha.pop() # pega o no mais exterior da pilha fica com -1)
                    for p in range(0, len(node_to)+1): # nao entendi o porque do + 1.
                        pilha.append(no_aux) 
                    #print("num de elem. empilhados:", len(node_to))
                    #print("pilha: ", spilha)               # o ou os cases deverao se conectar a no mais externo

        ########################################
        cria_link(node_from, node_to)

    if (len(pilha) != 0): # esse cara cria os links nos finais dos fluxos dos cases, ou do fluxo principals
        cria_link(node_to, pilha.pop())
        

def saida_links():
    # insere a tag links como ultimo elemento de root (<evaml>)
    # len(root) retorna o valor que sera o indice para o ultimo elemento
    tag_links = ET.Element("links") # cria a tag links (mae de varios links)
    root.insert(len(root), tag_links) #

    for i in range(len(links)): # insere cada link como os atributos from e to, dentro do elemento <links>
        tag_link = ET.Element("link", attrib={"from" : links[i].split(",")[0], "to" : links[i].split(",")[1]})
        root[len(root) - 1].insert(i, tag_link)

# processamento da interação
block_process(script_node) # true indica a geracao das keys

# gera os links
link_process(root.find("settings").find("voice"), script_node)

saida_links() # gera os links no arquivo xml

print("step 03 - Creating the Elements <link>...")

tree.write("_xml_links.xml")
