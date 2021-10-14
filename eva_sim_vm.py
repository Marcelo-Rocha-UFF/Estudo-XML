import random as rnd
import sys
import xml.etree.ElementTree as ET
import eva_memory

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
links_node = root.find("links")
fila_links =  [] # fila de links (comandos)
eva_global_var = []


# executa os comandos
def exec_comando(node):
	if node.tag == "voice":
		print("voice command")
		return True

	elif node.tag == "light":
		print("light command")
		return True

	elif node.tag == "wait":
		print("wait command")
		return True

	elif node.tag == "random":
		global eva_global_var # $ do software do robot no nodejs
		min = node.attrib["min"]
		max = node.attrib["max"]
		eva_memory.var_dolar.append(str(rnd.randint(int(min), int(max))))
		print("random command, min = " + min + ", max = " + max + ", valor = " + eva_memory.var_dolar[-1])
		return True

	elif node.tag == "listen":
		print("listen command")
		return True

	elif node.tag == "talk":
		print("talk command")
		return True

	elif node.tag == "userEmotion":
		print("userEmotion command")
		return True

	elif node.tag == "case":
		global fila_links
		valor = node.attrib["value"]
		print("valor ", valor, type(valor))
		if valor == eva_memory.var_dolar[-1]:
			node_tmp = fila_links[0] # guarda o no corrente em execucao
			fila_links = [] # esvazia a fila, pois o fluxo seguira deste no em diante
			fila_links.append(node_tmp) # add o no corrente na fila
			print("case command")
			return True
		else:
			return False


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
	anterior
	while len(fila_links) != 0:
		from_comando = fila_links[0].attrib["from"]
		comando_from = busca_commando(from_comando).tag # DEBUG

		# evita que um mesmo nó seja executado consecutivamente
		if anterior != from_comando:
			result = exec_comando(busca_commando(from_comando))
			anterior = from_comando
			
		if result == True:
				to_comando = fila_links[0].attrib["to"]
				comando_to = busca_commando(to_comando).tag # DEBUG
				fila_links.pop(0)
				if not(busca_links(to_comando)):
					exec_comando(busca_commando(to_comando))
					print("fim de bloco.............")
		else:
				fila_links.pop(0)
				print("false")


#busca_links("1000")
#link_process(-1)
