import hashlib

import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")

# funcao que gera as chaves para os elementos do script
def key_gen(script):
    key = 1000 # valor da primeira chave.
    root.find("settings").find("voice").attrib["key"] = str(key)
    key += 1
    # conjunto de nodes que nao recebem chaves.
    # A partir do dia 28-01-22 um switch passou a receber uma chave
    excluded_nodes = set(['script', 'stop', 'goto'])
    for node in script.iter():
        if not(node.tag in excluded_nodes):
            node.attrib["key"] = str(key)
            key += 1


# geracao das chaves identificadoras dos nodes
# estas chaves sao referenciadas nos links (elos) que conectam cada elemento (comando) do script
# os elementos script, switch, stop e goto nao possuem chaves

# Assume o default UTF-8 (Gera o id fazendo o hashing do nome do script para usar no db Json do Eva)
hash_object = hashlib.md5(root.attrib["name"].encode())
root.attrib["id"] = hash_object.hexdigest()

print("Step 02 - Generating Elements keys...")
key_gen(script_node)
tree.write("_node_keys.xml", "UTF-8")

