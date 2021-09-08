import sys
import json
import xml.etree.ElementTree as ET

tree = ET.parse("teste.xml")  # arquivo de codigo xml
root = tree.getroot() # evaml root node

qtd = len(root.find("interaction"))
interaction = root.find("interaction")
print("numero de nodes no bloco principal da interacao: ", qtd)

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


link_process(root.find("settings").find("voice"), interaction)
print("numero de arestas: ", len(links))
print(links)

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
    }"""

    return output

print(saida_links())
