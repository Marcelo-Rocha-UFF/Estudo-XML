import sys
import xml.etree.ElementTree as ET
import send_to_dbjson

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
output = ""
gohashid = 0

# percorre os elementos xml mapeando-os nos respectivos no modelo Json do Eva
def mapping_xml_to_json():
    global output
    # conjunto de nodes abstratos que nao sao mapeados no Json do robô
    excluded_nodes = set(['script', 'switch', 'stop', 'goto'])
    for elem in script_node.iter():
        if not(elem.tag in excluded_nodes):

            if (elem.tag == 'audio'):
                output += ",\n"
                output += audio_process(elem)

            if (elem.tag == 'light'):
                output += ",\n"
                output += light_process(elem)

            if (elem.tag == 'wait'):
                output += ",\n"
                output += wait_process(elem)

            if (elem.tag == 'talk'):
                output += ",\n"
                output += talk_process(elem)

            if (elem.tag == 'random'):
                output += ",\n"
                output += random_process(elem)

            if (elem.tag == 'listen'):
                output += ",\n"
                output += listen_process(elem)

            if (elem.tag == 'evaEmotion'):
                output += ",\n"
                output += eva_emotion_process(elem)

            if (elem.tag == 'case'):
                output += ",\n"
                output += case_process(elem)

            # default é um caso especial do comando case, onde value = ""
            if (elem.tag == 'default'):
                elem.attrib["value"] = ""
                output += ",\n"
                output += case_process(elem)


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
    return voice_process(node.find("voice"))
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
    color = light_command.attrib['color']
    color_map = {"white":"#ffffff", "black":"#000000", "red":"#ff0000", "pink":"#e6007e", "green":"#00ff00", "yellow":"#ffff00", "blue":"#0000ff"}
    if color_map.get(color) != None:
        color = color_map.get(color)
    light_node = """      {
        "key": """ + light_command.attrib["key"] + """,
        "name": "Light",
        "type": "light",
        "color": "lightblue",
        "isGroup": false,
        "group": "",
        "lcolor": """ + '"' + color + '",' + """
        "state": """ + '"' + light_command.attrib['state'] + '",' + """
        "__gohashid": """ + str(gohashid) + """
      }"""
    gohashid += 1
    return light_node

# listen node processing
def listen_process(listen_command):
    global gohashid
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
    global gohashid
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
    # speed 0 é o valor default. Não vejo necessidade de implementar isso

    if eva_emotion_command.attrib['emotion'] == "happy": # compatibiliza com o Eva. O Eva usa joy.
      eva_emotion_command.attrib['emotion'] = "joy"

    if eva_emotion_command.attrib['emotion'] == "angry": # compatibiliza com o Eva.
      eva_emotion_command.attrib['emotion'] = "anger"

    if eva_emotion_command.attrib['emotion'] == "neutral": # compatibiliza com o Eva.
      eva_emotion_command.attrib['emotion'] = "ini"

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
        

def saida_links():
    node_links = root.find("links")
    output ="""
      ],
      "link": [""" + """
        { 
          "from": """ + node_links[0].attrib["from"] + "," + """
          "to": """ + node_links[0].attrib["to"] + "," + """
          "__gohashid": 0
        }"""

    for i in range(len(node_links) - 1):
        output += """,
        { 
          "from": """ + node_links[i+1].attrib["from"] + "," + """
          "to": """ + node_links[i+1].attrib["to"] + "," + """
          "__gohashid": """ + str(i + 1) + """
        }"""

    output += """
      ]
    }
  }"""
  
    return output

# gerando o cabeçalho do Json
# onde são inseridos o id e o nome da interação baseados nos dados xml
output += head_process(root) # usa os atributos id e name da tag <evaml>

# o proximo comando pega o parametro do elemento voice (timbre) e gera o primeiro elem. do script Json
output += settings_process(root.find("settings"))

# processamento da interação
mapping_xml_to_json() # nova versao

# mapeia os links xml para json
output += saida_links()

print("step 04 - Mapping XML nodes and links to a JSON file...")

# criação de um arquivo físico da interação em Json
send_to_dbjson.create_json_file(root.attrib['name'], output)

# insere a interação no banco de interações do robo
#send_to_dbjson.send_to_dbjson(output)
