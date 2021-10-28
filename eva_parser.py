import os
import sys
import xml.etree.ElementTree as ET
import send_to_dbjson
import requests

# save to json flag
save = False

# run script in Eva Robot parameter
run = False

# read the command line parameters
for p in sys.argv:
	if p == '-s' or p == '-S':
		save = True
	if p == '-r' or p == '-R':
		run = True
	

# step 01 - expanding macros
cmd = "python3 eva_macro_exp.py " + sys.argv[1]
os.system(cmd)

# step 02 - generating keys
cmd = "python3 eva_node_keys.py _macro.xml"
os.system(cmd)

tree = ET.parse("_node_keys.xml")  #
root = tree.getroot() # evaml root node

# step 03 - to generate xml_exe file
cmd = "python3 eva_xml_links.py _node_keys.xml"
os.system(cmd)

# step 04 - generate the json file
cmd = "python3 eva_json_gen.py _xml_links.xml"
os.system(cmd)

# steps 5 and 6 (optional)
if save:
	# step 5 - send do json db
	with open(root.attrib['name'] + ".json", "r") as arqjson:
		output = arqjson.read()
	send_to_dbjson.send_to_dbjson(root.attrib['id'], root.attrib['name'], output)


if run:
	# step 6 run script
	key_value = {'id': root.attrib['id']} # parametros do request
	url_eva = 'http://192.168.1.100:3000/interaccion/iniciarInteracciong?'
	r = requests.get(url_eva, params = key_value)
	print("==> Runnig script: " + root.attrib['name'] + ", id: " + root.attrib['id'] + str(r))

