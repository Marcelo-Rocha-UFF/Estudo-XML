import copy # lib para a geracao de copias de objetos
import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
macros_node = root.find("macros")


###############################################################################
# Processamento (expansao) das macros                                         #
###############################################################################

def macro_expander(script_node, macros_node):
    for i in range(len(script_node)):
        if len(script_node[i]) != 0: macro_expander(script_node[i], macros_node)
        if script_node[i].tag == "useMacro":
            for m in range(len(macros_node)):
                if macros_node[m].attrib["name"] == script_node[i].attrib["name"]:
                    script_node.remove(script_node[i])
                    for j in range(len(macros_node[m])):
                        mac_elem_aux = copy.deepcopy(macros_node[m][j])
                        script_node.insert(i + j, mac_elem_aux)
                    break
            macro_expander(script_node, macros_node)
        #macro_expander(macros_node)
                    # mac_aux = copy.deepcopy(macros_node[m]) # duplica o obj.
                    # if script_node[i].get("id") != None: # se tem id, copia para primeiro elemento da macro
                    #     id_aux = script_node[i].attrib["id"]
                    #     script_node.remove(script_node[i])
                    #     script_node.insert(i, mac_aux)
                    #     script_node[i][0].attrib["id"] = id_aux
                    # else:
                    #     script_node.remove(script_node[i]) # expande sem inserir o id
                    #     script_node.insert(i, mac_aux)


# expande as macros
print("Step 01 - Processing Macros...")

# testa se a seção macro existe
if macros_node == None:
    print("  Warning -> The section macros does not exist.")
# testa se a seção está vazia
elif len(macros_node) == 0:
    print("  Warning -> There is no macro to be processed.")
    # processa a seção de macros
    macro_expander(script_node, macros_node)
    root.remove(macros_node) # remove a secao de macros


# gera o arquivo com as macros expandidas (caso existam) para a proxima etapa
tree.write("_macros.xml", "UTF-8")
