import sys
import json
import xml.etree.ElementTree as ET

tree = ET.parse("teste.xml")  # arquivo de codigo xml
root = tree.getroot() # evaml root node

# for elem in root.iter():
#     print(elem.tag)

inter = root.find("interaction")
mac = root.find("macros")
print("len de macros:", len(mac))

for i in range(len(inter)):
    if inter[i].tag == "use-macro":
        for m in range(len(mac)):
            if mac[m].get("label") == None:
                print("Nao tem label")
            else:
                print("Atributo da macro:", mac[m].get('label'))
            if mac[m].attrib["name"] == inter[i].attrib["name"]:
                inter.remove(inter[i])
                inter.insert(i, mac[m])
print("-------------------------------")



for elem in inter:
    if (elem.tag == "macro"):
        for e in elem:
            print("\t", e.tag)
    else:
        print(elem.tag)
    print("====================")
print("-------------------------------")

for i in range(len(inter)):
    print(inter[i].tag)
    # if inter[i].tag == "use-macro":
    #     print("macrooo")
print("-------------------------------")
