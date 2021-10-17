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
    #conjunto de nodes que nao recebem chaves
    excluded_nodes = set(['script', 'switch', 'stop', 'goto'])
    for node in script.iter():
        if not(node.tag in excluded_nodes):
            node.attrib["key"] = str(key)
            key += 1


# geracao das chaves identificadoras dos nodes
# estas chaves sao referenciadas nos links (elos) que conectam cada elemento (comando) do script
# os elementos switch, stop e goto nao possuem chaves
print("Step 02 - Generating Elements keys...")
key_gen(script_node)
tree.write("_node_keys.xml", "UTF-8")

