import sys
import json
import xml.etree.ElementTree as ET
tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
links_node = root.find("links")

def busca_command(key):
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

# varre os nodes buscando os comandos
for i in range(len(links_node)):
	node_from = links_node[i].attrib["from"]
	comando = busca_command(node_from)
	if comando != None:
		print(links_node[i].attrib, ", ", comando.tag)
