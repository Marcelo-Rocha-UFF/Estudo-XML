import sys
import json
import xml.etree.ElementTree as ET
import send_to_dbjson

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
output = ""
key = 1000
gohashid = 0
inicio = True  # para nao iniciar com a virgula

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

        if (command.tag == 'eva-emotion'):
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

# # tail processing
# def tail_process():
#     tail = """
#     ],
#     "link": []
#   }
# }"""
#     return tail


# audio node processing
def audio_process(audio_command):
    global gohashid, key
    audio_command.attrib["key"] = str(key)
    audio_node = """      {
        "key": """ + str(key) + """,
        "name": "Audio_0",
        "type": "sound",
        "color": "lightblue",
        "isGroup": false,
        "src": """ + '"' + audio_command.attrib['source'] + '",' + """
        "wait": """ + audio_command.attrib['wait'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    key += 1
    return audio_node

# light node processing
def light_process(light_command):
    global gohashid, key
    light_command.attrib["key"] = str(key)
    light_node = """      {
        "key": """ + str(key) + """,
        "name": "Light_8",
        "type": "light",
        "color": "lightblue",
        "isGroup": false,
        "group": "",
        "lcolor": """ + '"' + light_command.attrib['color'] + '",' + """
        "state": """ + '"' + light_command.attrib['state'] + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    key += 1
    return light_node

# listen node processing
def listen_process(listen_command):
    global gohashid, key
    listen_command.attrib["key"] = str(key)
    listen_node = """      {
        "key": """ + str(key) + """,
        "name": "Listen_8",
        "type": "listen",
        "color": "lightblue",
        "isGroup": false,
        "group": "",
        "lcolor": "zzz",
        "state": "zzz",
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    key += 1
    return listen_node


# talk node processing
def talk_process(talk_command):
    global gohashid, key
    talk_command.attrib["key"] = str(key)
    talk_node = """      {
        "key": """ + str(key) + """,
        "name": "Talk_1",
        "type": "speak",
        "color": "lightblue",
        "isGroup": false,
        "text": """ + '"' + talk_command.text + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    key += 1
    return talk_node


# voice node processing
def voice_process(voice_command):
    global gohashid, key
    voice_command.attrib["key"] = str(key)
    voice_node = """      {
        "key": """ + str(key) + """,
        "name": "Voice_1",
        "type": "voice",
        "color": "lightblue",
        "isGroup": false,
        "voice": """ + '"' + voice_command.attrib['tone'] + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    key += 1
    return voice_node


# eva_emotion node processing
def eva_emotion_process(eva_emotion_command):
    global gohashid, key
    eva_emotion_command.attrib["key"] = str(key)
    eva_emotion_node = """      {
        "key": """ + str(key) + """,
        "name": "Eva_Emotion_13",
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
    key += 1
    return eva_emotion_node


# random node processing
def random_process(random_command):
    global gohashid, key
    random_command.attrib["key"] = str(key)
    random_node = """      {
        "key": """ + str(key) + """,
        "name": "Random_10",
        "type": "random",
        "color": "lightblue",
        "isGroup": false,
        "group": "",
        "min": """ + random_command.attrib['min'] + ',' + """
        "max": """ + random_command.attrib['max'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    key += 1
    return random_node


# condition node (case and default) processing
def case_process(case_command):
    global gohashid, key
    case_command.attrib["key"] = str(key)
    case_node = """      {
        "key": """ + str(key) + """,
        "name": "Condition_2",
        "type": "if",
        "color": "lightblue",
        "isGroup": false,
        "text": """ + '"' + case_command.attrib['value'] + '",' + """
        "opt": 4,
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    key += 1
    return case_node

# wait node processing
def wait_process(wait_command):
    global gohashid, key
    wait_command.attrib["key"] = str(key)
    wait_node = """      {
        "key": """ + str(key) + """,
        "name": "Wait_2",
        "type": "wait",
        "color": "lightblue",
        "isGroup": false,
        "time": """ + wait_command.attrib['duration'] + ',' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    key += 1
    return wait_node



# gera os elos
qtd = len(root.find("interaction"))
interaction = root.find("interaction")
print("numero de nodes no bloco principal da interacao: ", qtd)

# aqui estão os métodos que geram os links que conectam os nós ################
links = []
def cria_link(node_from, node_to):
    # node goto
    if node_to.tag == "goto":
        for elem in interaction.iter():
            for at in elem.attrib:
                if at == "label":
                    if elem.attrib["label"] == node_to.attrib["target"]:
                        links.append(node_from.attrib["key"] + "," + elem.attrib["key"])
        return
    # um switch nunca pode ser from
    if node_from.tag == "switch": return
    # no "to" e uma folha, que nao contem filhos
    if len(node_to) == 0:
        links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])
    # trata os nodes com filhos
    elif (node_to.tag == "switch"): # trata o node "switch"
        for switch_elem in node_to:
            links.append(node_from.attrib["key"] + "," + switch_elem.attrib["key"])
            link_process(switch_elem, switch_elem)
    else: # outros casos de nodes com filhos, como o node do tipo "case"
        links.append(node_from.attrib["key"] + "," + node_to.attrib["key"])
        link_process(node_to, node_to)

def link_process(node_from, node_list):
    qtd = len(node_list)
    print("+", node_from.tag, node_list.tag, qtd, node_list[0].tag)
    node_to = node_list[0]
    print(node_from.tag, node_to.tag)
    cria_link(node_from, node_to)
    for i in range(0, qtd-1):
        node_from = node_list[i]
        node_to = node_list[i+1]
        print(node_from.tag, node_to.tag)
        cria_link(node_from, node_to)

def saida_links():
    output ="""   ],
        "link": [""" + """
        { "from": """ + links[0].split(",")[0] + "," + """
        "to": """ + links[0].split(",")[1] + "," + """
        "__gohashid": 0
        }"""

    for i in range(len(links)-1):
        output += """,
        { "from": """ + links[i+1].split(",")[0] + "," + """
        "to": """ + links[i+1].split(",")[1] + "," + """
        "__gohashid": """ + str(i + 1) + """
        }"""

    output += """
    ]
    }
    }"""

    return output

# gerando o cabeçalho do Json
# onde são inseridos o id e o nome da interação baseados nos dados xml
output += head_process(root.find("interaction"))

# o proximo comando pega o parametro do elemnto voice (timbre)
output += settings_process(root.find("settings"))

# processamento da interação
block_process(root.find("interaction"))

# gera os links
link_process(root.find("settings").find("voice"), interaction)
# print("numero de arestas: ", len(links))
# print(links)

# concatena a lista de links à lista de nós
output += saida_links()

# criação de um arquivo físico da interação em Json
send_to_dbjson.create_json_file(root.find("interaction").attrib['name'], output)

# insere a interação no banco de interações do robo
send_to_dbjson.send_to_dbjson(output)
