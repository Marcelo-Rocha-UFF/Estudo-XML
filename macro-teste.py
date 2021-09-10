import copy
import sys
import json
import xml.etree.ElementTree as ET

tree = ET.parse("macro.xml")  # arquivo de codigo xml
root = tree.getroot() # evaml root node

# for elem in root.iter():
#     print(elem.tag)

inter = root.find("interaction")
mac = root.find("macros")

for i in range(len(inter)):
    if inter[i].tag == "use-macro":
        for m in range(len(mac)):
            if mac[m].attrib["name"] == inter[i].attrib["name"]:
                if inter[i].get("id") != None: # se tem id, copia para primeiro elemento da macro
                    id_aux = inter[i].attrib["id"]
                    inter.remove(inter[i])
                    mac_aux = copy.deepcopy(mac[m])
                    inter.insert(i, mac_aux)
                    # tree.write("macro.xml")
                    # tree = ET.parse("macro.xml")  # arquivo de codigo xml
                    # root = tree.getroot() # evaml root node
                    # inter = root.find("interaction")
                    # mac = root.find("macros")
                    print(inter[i][0], " => ", mac[m][0])
                    inter[i][0].attrib["id"] = id_aux
                    print("use macro encontrado")
                    if mac[0][0].get("id") != None: print("Achei", i)
                else:
                    inter.remove(inter[i])
                    mac_aux = copy.deepcopy(mac[m])
                    inter.insert(i, mac_aux)
                    if mac[0][0].get("id") != None: print("sem id", i)


print("-------------------------------")


root.remove(mac)
print(inter[1].tag, inter[1].attrib)
#inter.remove(inter[1])
#inter.insert(1, mac[0])
#inter[1][0].set("id", "INICIO")

tree.write("teste.xml")

for elem in root.iter():
    print(elem.tag, elem.attrib)
