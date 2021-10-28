import sys
import xml.etree.ElementTree as ET
import send_to_dbjson

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node


dbfile = open('db.json', 'r')

# insere o script no banco de scripts do robo
send_to_dbjson.send_to_dbjson(root.attrib['id'], root.attrib['name'], output)
