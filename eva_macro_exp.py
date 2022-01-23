"""
Nesta etapa, caso o script contenha o comando <useMacro>, o parser acusa um erro,
caso não  haja a seção macros e também, caso não haja macros definidas.
Ele também acusa um erro, caso o comando <useMacro> faça referência a uma macro que não foi definida.
O parser indica o nome da macro que não foi encontrada.
Uma definição de macro não pode ser vazia (isso não faria sentido).
Caso algum comando <useMacro> faça referência a uma macro com zero elementos o parser vai indicar o erro.
O parser substitui a tag <useMacro> com problema, por uma tag <error> indicando o tipo do erro,
nesse caso “undefined_macro”, o nome da macro não definida e escreve essa informação no no arquivo de saída da etapa.
 """

import copy # lib para a geracao de copias de objetos
import sys
import xml.etree.ElementTree as ET

tree = ET.parse(sys.argv[1])  # arquivo de codigo xml
root = tree.getroot() # evaml root node
script_node = root.find("script")
macros_node = root.find("macros")
_error = 0 # 0 indica que não houve falha na etapa. 

###############################################################################
# Processamento (expansao) das macros                                         #
###############################################################################

def macro_expander(script_node, macros_node):
    global _error
    for i in range(len(script_node)):
        if len(script_node[i]) != 0: macro_expander(script_node[i], macros_node)
        if script_node[i].tag == "useMacro":
            if (macros_node == None): # testa se a seção macros foi criada
                print("  Error -> You are using <useMacro> but the section macros does not exist.")
                _error = 1 # falha
                break
            elif (len(macros_node) == 0): # nenhuma macro foi definida
                print("  Error -> You are using <useMacro> but no macro was defined.")
                _error = 1 # falha
                break
            match_macro = False
            for m in range(len(macros_node)):
                if macros_node[m].attrib["name"] == script_node[i].attrib["name"]:
                    match_macro = True
                    if (len(macros_node[m])) == 0:
                        script_node[i].tag = "error"
                        _error = 1 # falha
                        script_node[i].attrib["type"] = "macro_is_empty"
                        script_node[i].attrib["macro_name"] = script_node[i].attrib["name"]
                        print("  Error -> The macro", macros_node[m].attrib["name"], "is empty..." )
                        script_node[i].attrib.pop("name")
                    else:
                        script_node.remove(script_node[i])

                    for j in range(len(macros_node[m])):
                        mac_elem_aux = copy.deepcopy(macros_node[m][j])
                        script_node.insert(i + j, mac_elem_aux)
                    break      
            if match_macro == False: # caso o nome da macro não seja encontrado nas macros
                script_node[i].tag = "error"
                _error = 1 # falha
                script_node[i].attrib["type"] = "undefined_macro"
                script_node[i].attrib["macro_name"] = script_node[i].attrib["name"]
                print("  Error -> The <useMacro> references a macro that has not been defined:", script_node[i].attrib["name"])
                script_node[i].attrib.pop("name")  
            
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
#if macros_node == None:
#    print("  Warning -> The section macros does not exist.")
# testa se a seção está vazia
#elif len(macros_node) == 0:
#    print("  Warning -> The macros section exists but is empty.")
#else: 
#    print()
    # processa a seção de macros
    
macro_expander(script_node, macros_node)
if macros_node != None:
    root.remove(macros_node) # remove a secao de macros, caso ela exista

# gera o arquivo com as macros expandidas (caso existam) para a proxima etapa
tree.write("_macros.xml", "UTF-8")

exit(_error) # termina a execução indicando se houve erro (1) ou não (0)
