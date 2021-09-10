import sys
import json
import xml.etree.ElementTree as ET

tree = ET.parse("macro.xml")  # arquivo de codigo xml
root = tree.getroot() # evaml root node

# for elem in root.iter():
#     print(elem.tag)

interaction_node = root.find("interaction")

for e in interaction_node:
    print(e.tag, e.attrib)
