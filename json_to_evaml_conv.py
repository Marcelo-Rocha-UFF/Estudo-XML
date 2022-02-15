import json
import xml.etree.ElementTree as ET
import re # expressão regular
from pprint import pprint

from click import command # pode retirar depois


# lendo do arquivo json
with open('script20.json', 'r') as openfile:
  json_object = json.load(openfile) # é um dict.
    
comandos_json = json_object["data"]["node"] # Lista de nós. Cada nó (um comando) é um dict. com os seus pares chave/valor do respectivo elemento.
links_json = json_object["data"]["link"] # Lista de links. Cada link é um dict. com as chaves "from" e "to"
print(json_object.keys(),"\n")
print(comandos_json,"\n")
print(links_json)

# cria o elemento raiz <evaml> e seus subelementos
evaml_atributos = {"name":json_object["nombre"]}
evaml = ET.Element("evaml", evaml_atributos )
#
settings = ET.SubElement(evaml, "settings")
# add os subelementos de settings com seus atributos
for comando in comandos_json:
  if comando["name"] == "Voice": # busca comando voice e seus atributos
    voice_atributos = {"tone":comando["voice"], "key":str(comando["key"])}

voice = ET.SubElement(settings, "voice", voice_atributos)

# este elementos ficam com os valores default pois ainda não foram implementados no robô
lightEffects_atributos = {"mode":"on"}
lightEffects = ET.SubElement(settings, "lightEffects", lightEffects_atributos)

audioEffects_atributos = {"mode":"on",  "vol":"100%"}
audioEffects = ET.SubElement(settings, "audioEffects", audioEffects_atributos)

# 
script = ET.SubElement(evaml, "script")
links = ET.SubElement(evaml, "links")

# processamentos dos comandos no arquivo json
def processa_nodes(script, comandos_json):
  for comando in comandos_json:

    # <light>
    if comando["type"] == "light":
      light_atributos = {"key" : str(comando["key"]), "state" : comando["state"], "color" : comando["color"]}
      ET.SubElement(script, "light", light_atributos)
  

    # <audio>
    if comando["type"] == "sound":
      audio_atributos = {"key" : str(comando["key"]), "source" : comando["src"], "block" : str(comando["wait"]).lower()}
      ET.SubElement(script, "audio", audio_atributos)


    # <evaEmotion>
    if comando["type"] == "emotion":
      # mapeando os nomes da expressões (4 expressões)
      if (comando["emotion"] == "anger"): eva_emotion = "angry"
      elif (comando["emotion"] == "joy"): eva_emotion = "happy"
      elif (comando["emotion"] == "ini"): eva_emotion = "neutral"
      else: eva_emotion = "sad"

      eva_emotion_atributos = {"key" : str(comando["key"]), "emotion" :eva_emotion}
      ET.SubElement(script, "evaEmotion", eva_emotion_atributos)

    # <leds>
    if comando["type"] == "led":
      # mapeando os nomes da expressões (4 expressões)
      if (comando["anim"] == "anger"): animatiom = "angry"
      elif (comando["anim"] == "joy"): animatiom = "happy"
      elif (comando["anim"] == "escuchaT"): animatiom = "listen"
      elif (comando["anim"] == "sad"): animatiom = "sad"
      elif (comando["anim"] == "hablaT_v2"): animatiom = "speak"
      elif (comando["anim"] == "stop"): animatiom = "stop"
      elif (comando["anim"] == "surprise"): animatiom = "surprise"

      led_atributos = {"key" : str(comando["key"]), "animation" :animatiom}
      ET.SubElement(script, "led", led_atributos)


    # <wait>
    if comando["type"] == "wait":
      wait_atributos = {"key" : str(comando["key"]), "duration" : str(comando["time"])}
      ET.SubElement(script, "wait", wait_atributos)

    
    # <listen>
    if comando["type"] == "listen":
      listen_atributos = {"key" : str(comando["key"])}
      ET.SubElement(script, "listen", listen_atributos)

    
    # <random>
    if comando["type"] == "random":
      random_atributos = {"key" : str(comando["key"]), "min" : str(comando["min"]), "max" : str(comando["max"])}
      ET.SubElement(script, "random", random_atributos)


    # <talk>
    if comando["type"] == "speak":
      speak_atributos = {"key" : str(comando["key"])}
      talk = ET.SubElement(script, "talk", speak_atributos)
      talk.text = comando["text"]


    # <userEmotion>
    if comando["type"] == "user_emotion":
      user_emotion_atributos = {"key" : str(comando["key"])}
      ET.SubElement(script, "userEmotion", user_emotion_atributos)


    # <counter>
    if comando["type"] == "counter":
      # mapping operations types
      if (comando["ops"] == "assign"): op = "="
      elif (comando["ops"] == "rest"): op = "%"
      elif (comando["ops"] == "mul"): op = "*"
      elif (comando["ops"] == "sum"): op = "+"
      elif (comando["ops"] == "div"): op = "/"

      counter_atributos = {"key" : str(comando["key"]), "var" : comando["count"], "op" : op , "value" : str(comando["value"])}
      ET.SubElement(script, "counter", counter_atributos)



    # <if>
    if comando["type"] == "if":
      tag = "case" # a tag padrão é a case
      # mapping "op" types
      if (comando["opt"]) == 4: # exact com $
        op = "exact" # exact
        value = comando["text"]
        if (value == ""): # caso op seja exact e value "", identifica o condicion como default. Isso gera uma restrição na construção de scripts usando a VPL
          tag = "default"
        var = "$"
      elif (comando["opt"]) == 2: # contain com $
        op = "contain"
        value = comando["text"]
        var = "$"
      elif (comando["opt"]) == 5: # eq com #variavel
        if ("==" in comando["text"]): op = "eq"
        elif (">=" in comando["text"]): op = "gte"
        elif ("<=" in comando["text"]): op = "lte"
        elif ("!=" in comando["text"]): op = "ne"
        elif (">" in comando["text"]): op = "gt"
        elif ("<" in comando["text"]): op = "lt"

        # com opt igual 5, comando["text"] tem algo desse tipo #x == 2 ou $ == 2(comparação matematica)
        # a exp reg, por padrao, ret uma lista. Pegamos o prim. e unico elemento, a partir do seg. caract. ou seja, depois do "#"
        if ("$" in comando["text"]):
          var = "$" # comparacao com dolar
        else:
          var = (re.findall(r'\#[a-zA-Z]+[0-9]*', comando["text"]))[0][1:] # comparacao com variavel

        value = (re.findall(r'[0-9]+', comando["text"]))[0]
      if_atributos = {"key" : str(comando["key"]), "op" : op, "value" : value, "var" : var}
      ET.SubElement(script, tag , if_atributos)

      #<case op="eq" value="1" key="1034" child_proc="true" var="$">



# processamentos dos links no arquivo json
def processa_links(links, links_json):
  for link in links_json:
    link_atributos = {"from" : str(link["from"]), "to" : str(link["to"])}
    ET.SubElement(links, "link", link_atributos)

  # somente para impressão
  xml_processed = ET.tostring(evaml, encoding='utf8').decode('utf8')
  with open("JSON_TO_EvaML.xml", "w") as text_file: # grava o xml processado (temporario) em um arquivo para ser importado pelo parser
      text_file.write(xml_processed)
  pprint(xml_processed)



processa_nodes(script, comandos_json)
processa_links(links, links_json)
#ET.dump(evaml)