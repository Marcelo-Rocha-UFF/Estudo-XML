import random as rnd
import sys
import xml.etree.ElementTree as ET
import eva_memory


tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
links_node = root.find("links")
fila_links =  [] # fila de links (comandos)

# executa os comandos
def exec_comando(node):
	if node.tag == "voice":
		print("voice command")

	elif node.tag == "light":
		print("light command")

	elif node.tag == "wait":
		print("wait command")

	elif node.tag == "random":
		min = node.attrib["min"]
		max = node.attrib["max"]
		eva_memory.var_dolar.append(str(rnd.randint(int(min), int(max))))
		print("random command, min = " + min + ", max = " + max + ", valor = " + eva_memory.var_dolar[-1])

	elif node.tag == "listen":
		print("listen command")

	elif node.tag == "talk":
		print("talk command")

	elif node.tag == "userEmotion":
		print("userEmotion command")

	elif node.tag == "case":
		eva_memory.reg_case = 0 # limpa o flag do case
		valor = node.attrib["value"]
		print("valor ", valor, type(valor))
		if valor == eva_memory.var_dolar[-1]:
			eva_memory.reg_case = 1 # liga o reg case indicando que o resultado da comparacao foi verdadeira


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


busca_links("1000")
link_process(-1)
