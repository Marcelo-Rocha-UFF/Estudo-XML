from os import link
import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
links_node = root.find("links")
fila_links =  [] # fila de links (comandos)

def voice():
	print("voice command")

def light():
	print("light command")

def wait():
	print("wait command")

def random():
	print("random command")

def listen():
	print("listen command")

def talk():
	print("talk command")

def case():
	print("case command")

# executa os comandos
def exec_comando(node):
	if node.tag == "voice":
		voice()
	elif node.tag == "light":
		light()
	elif node.tag == "wait":
		wait()
	elif node.tag == "random":
		random()
	elif node.tag == "listen":
		listen()
	elif node.tag == "talk":
		talk()
	elif node.tag == "case":
		case()

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

# varre os nodes buscando os comandos
# for i in range(len(links_node)):
# 	node_from = links_node[i].attrib["from"]
# 	comando = busca_command(node_from)
# 	if comando != None:
# 		print(links_node[i].attrib, ", ", comando.tag)



# executa os comandos que estão na pilha de links
def link_process():
	global anterior
	from_comando = fila_links[0].attrib["from"]
	# evita que um mesmo nó seja executado consecutivamente
	if anterior != from_comando:
		exec_comando(busca_commando(from_comando))
		anterior = from_comando
	while len(fila_links) != 0:
		to_comando = fila_links[0].attrib["to"]
		fila_links.pop(0)
		if not(busca_links(to_comando)):
			exec_comando(busca_commando(to_comando))
			print("fim de bloco.............")
			return
		else:
			link_process()


anterior = -1
busca_links("1000")
link_process()
