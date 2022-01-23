import os
import sys
import ctypes
import xml.etree.ElementTree as ET
import eva_send_to_dbjson
import requests
import time

# This function gets the python command name used in command line
def get_python_interpreter_arguments():
  argc = ctypes.c_int()
  argv = ctypes.POINTER(ctypes.c_wchar_p if sys.version_info >= (3, ) else ctypes.c_char_p)()
  ctypes.pythonapi.Py_GetArgcArgv(ctypes.byref(argc), ctypes.byref(argv))
  arguments = list()
  for i in range(argc.value - len(sys.argv) + 1):
    arguments.append(argv[i])
  return arguments

# save to json flag
save = False

# run script in Eva Robot parameter
run = False

# compile the script
compile = False

# read the command line parameters
for p in sys.argv:
	if p == '-s' or p == '-S':
		save = True
	elif p == '-r' or p == '-R':
		run = True
	elif p == '-c' or p == '-C':
		compile = True
	
if compile:
	# Now, each step only run if the previous step was OK
	# step 01 - expanding macros
	cmd = get_python_interpreter_arguments()[0] + " eva_macro_exp.py " + sys.argv[1]
	if (os.system(cmd)) == 0: # step 01 OK
		# step 02 - generating keys
		cmd = get_python_interpreter_arguments()[0] + " eva_node_keys.py _macros.xml"
		if (os.system(cmd)) == 0: # step 02 OK
			# step 03 - to generate xml_exe file
			cmd = get_python_interpreter_arguments()[0] + " eva_xml_links.py _node_keys.xml"
			if (os.system(cmd)) == 0: # step 03 OK
				# step 04 - generate the json file
				tree = ET.parse("_node_keys.xml")  #
				root = tree.getroot() # evaml root node
				cmd = get_python_interpreter_arguments()[0] + " eva_json_gen.py " + root.attrib['name'] + "_EvaML.xml" #_xml_links.xml"
				os.system(cmd)

# steps 5 and 6 (optional)
if save:
	tree = ET.parse("_node_keys.xml")  #
	root = tree.getroot() # evaml root node
	# step 5 - send do json db
	with open(root.attrib['name'] + ".json", "r") as arqjson:
		output = arqjson.read()
	eva_send_to_dbjson.send_to_dbjson(root.attrib['id'], root.attrib['name'], output)
	

if run:
	# step 6 run script
	tree = ET.parse("_node_keys.xml")  #
	root = tree.getroot() # evaml root node
	if save or compile:
		time.sleep(3) # tempo necessário para o restart do serviço do Eva
	key_value = {'id': root.attrib['id']} # parametros do request
	url_eva = 'http://192.168.1.100:3000/interaccion/iniciarInteracciong?'
	r = requests.get(url_eva, params = key_value)
	print("==> Runnig script: " + root.attrib['name'] + ", id: " + root.attrib['id'])

