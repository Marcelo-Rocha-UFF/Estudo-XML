import random as rnd
import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
links_node = root.find("links")
fila_links =  [] # fila de links (comandos)
eva_global_var = []

def voice():
	print("voice command")
	return True

def light():
	print("light command")
	return True

def wait():
	print("wait command")
	return True

def random(min, max):
	global eva_global_var # $ do software do robot no nodejs
	eva_global_var = str(rnd.randint(int(min), int(max)))
	print("random command, min = " + min + ", max = " + max + ", valor = " + eva_global_var[-1])
	return True

def listen():
	print("listen command")
	return True

def talk():
	print("talk command")
	return True

def userEmotion():
	print("userEmotion command")
	return True

def case(value):
	global fila_links
	print("valor ", value, type(value))
	if value == eva_global_var:
		node_tmp = fila_links[0] # guarda o no corrente em execucao
		fila_links = [] # esvazia a fila
		fila_links.append(node_tmp) # add o no corrente na fila
		print("case command")
		return True
	else:
		return False
	

# executa os comandos
def exec_comando(node):
	if node.tag == "voice":
		return voice()

	elif node.tag == "light":
		return light()

	elif node.tag == "wait":
		return wait()

	elif node.tag == "random":
		return random(node.attrib["min"], node.attrib["max"])

	elif node.tag == "listen":
		return listen()

	elif node.tag == "talk":
		return talk()

	elif node.tag == "userEmotion":
		return userEmotion()

	elif node.tag == "case":
		return case(node.attrib["value"])


def busca_commando(key):
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
def link_process():
	global anterior
	while len(fila_links) != 0:
		from_comando = fila_links[0].attrib["from"]
		# evita que um mesmo nó seja executado consecutivamente
		if anterior != from_comando:
			result = exec_comando(busca_commando(from_comando))
			anterior = from_comando
			
		if result == True:
				to_comando = fila_links[0].attrib["to"]
				fila_links.pop(0)
				if not(busca_links(to_comando)):
					exec_comando(busca_commando(to_comando))
					print("fim de bloco.............")
		else:
				anterior = from_comando
				fila_links.pop(0)
				print("false")




anterior = -1
busca_links("1000")
link_process()
